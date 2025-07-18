from langgraph.graph import StateGraph, END, START
import os
from .state import ResearchState
from workstation.components.retriever import build_hybrid_retriever
from workstation.components.financials import get_financial_data
from workstation.components.analyst import run_analysis
from workstation.components.charting import create_and_save_charts

# --- Node Functions ---

def run_qualitative_research(state: ResearchState):
    """Node for qualitative research."""
    print("--- Starting Qualitative Research Node (News Desk) ---")
    topic = state['topic']
    retriever = build_hybrid_retriever(topic)
    return {"qualitative_data_retriever": retriever}

def run_quantitative_research(state: ResearchState):
    """Node for quantitative research."""
    print("--- Starting Quantitative Research Node (Quant Desk) ---")
    ticker = state['ticker']
    data = get_financial_data(ticker)
    return {"quantitative_data": data}

def run_analysis_node(state: ResearchState):
    """Node for running the analysis."""
    analysis_results = run_analysis(state)
    return {
        "analysis": analysis_results["analysis"],
        "chart_data": analysis_results["chart_data"]
    }

def run_chart_generator_node(state: ResearchState):
    """Node for generating and saving charts."""
    chart_paths = create_and_save_charts(state["chart_data"], state["quantitative_data"])
    return {"chart_image_paths": chart_paths}

def run_report_writer_node(state: ResearchState):
    """Node for compiling the final markdown report and saving it to a file."""
    print("--- Compiling and Saving Final Report ---")
    analysis = state.get("analysis", "No analysis was generated.")
    chart_paths = state.get("chart_image_paths", [])
    
    report_content = f"# Financial Research Report: {state['topic']}\n\n"
    report_content += analysis
    
    if chart_paths:
        report_content += "\n\n## Visualizations\n\n"
        for path in chart_paths:
            # Create a robust, cross-platform relative path for the markdown link
            relative_path = os.path.basename(path)
            posix_path = relative_path.replace('\\', '/')
            report_content += f"![Chart](./{posix_path})\n"
            
    # Save the report file
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    report_path = os.path.join(output_dir, "financial_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"   ✅ Final report saved to: {report_path}")
            
    return {"report_path": report_path}

def join_branches(state: ResearchState):
    """A synchronization point for parallel branches."""
    print("--- Joining parallel branches ---")
    return {}

# --- Conditional Logic ---

def should_continue(state: ResearchState):
    """Determines whether to continue to the analysis step or end."""
    if state.get('qualitative_data_retriever') and state.get('quantitative_data'):
        print("--- Data gathering complete. Proceeding to analysis. ---")
        return "continue"
    else:
        print("--- Missing data from one or more sources. Ending workflow. ---")
        return "end"

# --- Graph Builder ---

def build_graph():
    """Builds the multi-agent workflow using LangGraph."""
    workflow = StateGraph(ResearchState)

    # Define all nodes
    workflow.add_node("qualitative_research", run_qualitative_research)
    workflow.add_node("quantitative_research", run_quantitative_research)
    workflow.add_node("joiner", join_branches)
    workflow.add_node("analysis", run_analysis_node)
    workflow.add_node("chart_generator", run_chart_generator_node)
    workflow.add_node("report_writer", run_report_writer_node)

    # Build the graph flow
    workflow.add_edge(START, "qualitative_research")
    workflow.add_edge(START, "quantitative_research")
    workflow.add_edge("qualitative_research", "joiner")
    workflow.add_edge("quantitative_research", "joiner")
    
    workflow.add_conditional_edges(
        "joiner",
        should_continue,
        {"continue": "analysis", "end": END}
    )
    
    workflow.add_edge("analysis", "chart_generator")
    workflow.add_edge("chart_generator", "report_writer")
    workflow.add_edge("report_writer", END)

    # Compile the graph
    return workflow.compile()
