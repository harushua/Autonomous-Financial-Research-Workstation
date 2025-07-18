
# 🤖 Autonomous Financial Research Workstation

Automate financial research with a multi-agent AI system. Provide a company ticker and research topic—get a comprehensive, data-driven report with charts and sources.

---

## Features

- **Multi-Agent Collaboration:** Specialized agents (Researcher, Analyst, Chart Generator) work together.
- **Parallel Data Gathering:** Fetches news and financial data simultaneously.
- **Hybrid Search:** Combines BM25 (keyword) and FAISS (semantic) for relevant context.
- **Source-Cited Analysis:** Every claim is cited with its source URL.
- **Automated Visuals:** Generates and embeds charts in the report.
- **End-to-End Automation:** From query to polished Markdown report in one run.

---

## Architecture & Workflow

1. **User Input:** Company ticker (e.g., `NVDA`) and research topic.
2. **Parallel Data Gathering:**
    - *Qualitative:* Web search (Tavily) → Web scrape (Firecrawl) → Index (FAISS/BM25)
    - *Quantitative:* Financial data fetch (Polygon.io)
3. **Sync:** Wait for both arms to finish.
4. **Analysis:** Lead Analyst agent synthesizes and cites findings.
5. **Report Generation:**
    - Chart Generator creates images (Matplotlib)
    - Report Writer compiles everything into Markdown

---

## Tech Stack

- LangGraph (orchestration)
- LangChain (AI framework)
- OpenAI GPT-4o (LLM)
- Tavily Search (web search)
- Firecrawl (web scraping)
- Polygon.io (financial data)
- FAISS, rank-bm25 (search)
- Matplotlib (charts)
- Python
- uv (package management)

---

## Quickstart

```sh
# 1. Clone
git clone https://github.com/harushua/Autonomous-Financial-Research-Workstation.git
cd autonomous-financial-workstation

# 2. Environment
python -m venv .venv
# Activate:
#   Windows: .venv\Scripts\activate
#   Mac/Linux: source .venv/bin/activate

# 3. Install dependencies
uv pip install -r requirements.txt

# 4. Add API keys (.env in project root)
# Example:
# OPENAI_API_KEY="sk-..."
# TAVILY_API_KEY="tvly-..."
# FIRECRAWL_API_KEY="fc-..."
# POLYGON_API_KEY="..."

# 5. Run
python main.py
```

Output: Markdown report and charts in the `outputs/` folder.

---

## Project Structure

```text
autonomous-financial-workstation/
├── main.py
├── requirements.txt
├── outputs/
│   ├── quarterly_revenue.png
│   └── financial_report.md
└── workstation/
    ├── components/
    │   ├── analyst.py
    │   ├── charting.py
    │   ├── financials.py
    │   └── retriever.py
    └── graph/
        ├── builder.py
        └── state.py
```
