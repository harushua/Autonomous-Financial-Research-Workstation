import json
from operator import itemgetter

# FIX: Import JsonOutputParser for more reliable output handling
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from workstation.graph.state import ResearchState

def get_analyst_llm():
    """Initializes and returns the ChatOpenAI model for the analyst."""
    return ChatOpenAI(model_name="gpt-4o", temperature=0)

def format_analysis_to_markdown(analysis_json: dict) -> str:
    """Formats the structured analysis JSON into a readable markdown string."""
    output = []
    if "executive_summary" in analysis_json:
        output.append(f"## Executive Summary\n\n{analysis_json['executive_summary']}")
    
    if "swot_analysis" in analysis_json:
        swot = analysis_json["swot_analysis"]
        output.append("\n## SWOT Analysis")
        output.append("\n### Strengths\n" + "\n".join(f"- {s}" for s in swot.get("strengths", [])))
        output.append("\n### Weaknesses\n" + "\n".join(f"- {w}" for w in swot.get("weaknesses", [])))
        output.append("\n### Opportunities\n" + "\n".join(f"- {o}" for o in swot.get("opportunities", [])))
        output.append("\n### Threats\n" + "\n".join(f"- {t}" for t in swot.get("threats", [])))
        
    if "market_outlook" in analysis_json:
        output.append(f"\n## Market Outlook\n\n{analysis_json['market_outlook']}")
        
    return "\n".join(output)

def run_analysis(state: ResearchState):
    """
    Performs the core analysis by synthesizing qualitative and quantitative data.
    """
    print("--- Running Analysis Node (Lead Analyst) ---")
    
    if not state.get("qualitative_data_retriever") or not state.get("quantitative_data"):
        print("   ❌ Missing data for analysis. Ending workflow.")
        return {"analysis": "Error: Missing data for analysis.", "chart_data": []}

    retriever = state["qualitative_data_retriever"]
    financial_data = state["quantitative_data"]
    topic = state["topic"]
    
    quant_summary = json.dumps(financial_data, indent=2)[:4000]

    # FIX: Updated prompt to request a single, structured JSON object.
    # This is much more reliable than splitting a string.
    prompt_template = """
    You are a world-class financial analyst. Your task is to provide a detailed, data-driven analysis for the following topic: "{topic}"

    You must synthesize information from two sources:
    1.  **Qualitative Context**: Recent news and articles, which you can access using the provided retriever.
    2.  **Quantitative Context**: Key financial metrics and news headlines, provided below.

    **Quantitative Data Summary:**
    ```json
    {quant_summary}
    ```

    **Qualitative Context (use the retriever for this):**
    {context}

    **Instructions:**
    Based on all the provided context, generate a final report.
    For every statement you make, you **must** cite the source from the qualitative context's metadata.
    
    **Output Format (Return ONLY a single valid JSON object with the following keys):**
    ```json
    {{
        "analysis": {{
            "executive_summary": "A concise overview of the findings.",
            "swot_analysis": {{
                "strengths": ["List of strengths with citations"],
                "weaknesses": ["List of weaknesses with citations"],
                "opportunities": ["List of opportunities with citations"],
                "threats": ["List of threats with citations"]
            }},
            "market_outlook": "Your detailed market outlook with citations."
        }},
        "charts": [
            {{"title": "Quarterly Revenue", "query_for_data": "A specific query to get revenue data for a chart"}},
            {{"title": "Net Income", "query_for_data": "A specific query to get net income data for a chart"}}
        ]
    }}
    ```
    """
    
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm = get_analyst_llm()
    # FIX: Use JsonOutputParser to reliably get a dictionary from the LLM.
    output_parser = JsonOutputParser()

    rag_chain = (
        {
            "context": itemgetter("topic") | retriever,
            "topic": itemgetter("topic"),
            "quant_summary": itemgetter("quant_summary"),
        }
        | prompt
        | llm
        | output_parser # Use the new parser
    )

    try:
        # The chain now directly outputs a dictionary
        full_response_dict = rag_chain.invoke({"topic": topic, "quant_summary": quant_summary})
        
        # Format the structured analysis into a readable string
        analysis_text = format_analysis_to_markdown(full_response_dict.get("analysis", {}))
        chart_data = full_response_dict.get("charts", [])

    except Exception as e:
        print(f"   ❌ Error during analysis chain invocation: {e}")
        analysis_text = "Error: Could not generate the analysis."
        chart_data = []

    return {
        "analysis": analysis_text,
        "chart_data": chart_data
    }
