🤖 Autonomous Financial Research Workstation
This project is a sophisticated multi-agent system designed to automate the entire financial research process. Given a company ticker and a research topic, the system autonomously gathers, analyzes, and synthesizes both qualitative and quantitative data to generate a comprehensive, data-driven report complete with visualizations.

The architecture is a modular monolith, orchestrated by LangGraph, ensuring a clean separation of concerns while maintaining the simplicity of a single application.

✨ Features
Multi-Agent Architecture: Utilizes a team of specialized AI agents (e.g., Researcher, Analyst, Chart Generator) that collaborate to perform complex tasks.

Parallel Data Gathering: Simultaneously fetches unstructured news articles and structured financial data to maximize efficiency.

Advanced Hybrid Search: Implements a powerful Retrieval-Augmented Generation (RAG) pipeline using a hybrid of BM25 (keyword) and FAISS (semantic) search for highly relevant context.

Source-Cited Analysis: The lead analyst agent provides a detailed report (Executive Summary, SWOT, Outlook) and cites the source URL for every claim it makes.

Automated Visualizations: Dynamically generates and embeds relevant charts (e.g., Quarterly Revenue) directly into the final report.

End-to-End Automation: From a single query, the system handles everything from data discovery to saving the final, polished Markdown report.

⚙️ Architecture & Workflow
The system is orchestrated by LangGraph as a state machine. The workflow proceeds as follows:

Initiation: The user provides a company ticker (e.g., NVDA) and a research topic.

Parallel Data Gathering:

Qualitative Arm (News Desk): A Web_Searcher agent uses Tavily to find relevant URLs, which are then passed to a Web_Scraper that uses Firecrawl to extract the full article content. The content is then indexed by an Indexer into a hybrid FAISS/BM25 retriever.

Quantitative Arm (Quant Desk): A Financial_Data_Fetcher agent uses the Polygon.io API to retrieve financial statements, historical data, and ticker-specific news.

Synchronization: A joiner node waits for both parallel branches to complete before proceeding.

Synthesis & Analysis: A Lead_Analyst agent receives the hybrid retriever and the structured financial data. It performs RAG to generate a detailed analysis and identify key metrics for visualization.

Report Generation:

A Chart_Generator agent uses Matplotlib to create and save chart images based on the analyst's findings.

A final Report_Writer agent compiles the analysis and embeds the chart images into a single, clean Markdown file.

🛠️ Technology Stack
Orchestration: LangGraph

AI Framework: LangChain

LLM: OpenAI GPT-4o

Web Search: Tavily Search

Web Scraping: Firecrawl

Financial Data API: Polygon.io

Vector Store / Search: FAISS (for semantic search), rank-bm25 (for keyword search)

Data Visualization: Matplotlib

Core Language: Python

Package Management: uv

🚀 Setup and Installation
1. Clone the Repository
git clone https://github.com/harushua/Autonomous-Financial-Research-Workstation.git
cd autonomous-financial-workstation

2. Set Up the Environment
This project uses uv for package management.

# Create a virtual environment
python -m venv .venv

# Activate the environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

3. Install Dependencies
Install all required packages from the requirements.txt file.

uv pip install -r requirements.txt

4. Configure API Keys
Create a .env file in the root of the project and add your API keys.

# .env

# Get from https://platform.openai.com/
OPENAI_API_KEY="sk-..."

# Get from https://app.tavily.com/
TAVILY_API_KEY="tvly-..."

# Get from https://firecrawl.dev/
FIRECRAWL_API_KEY="fc-..."

# Get from https://polygon.io/
POLYGON_API_KEY="..."

▶️ How to Run
Execute the main.py script from the root directory to start the research process.

python main.py

The workflow will run, printing its progress to the console. Upon completion, a financial_report.md file and an outputs directory containing the chart images will be saved in your project folder.

📂 Project Structure
autonomous-financial-workstation/
├── .env
├── main.py                 # Main entry point to run the application
├── requirements.txt        # Project dependencies
├── outputs/                # Directory for generated charts and reports
│   ├── quarterly_revenue.png
│   └── financial_report.md
└── workstation/
    ├── __init__.py
    ├── components/         # Reusable, self-contained logic modules
    │   ├── __init__.py
    │   ├── analyst.py
    │   ├── charting.py
    │   ├── financials.py
    │   └── retriever.py
    └── graph/              # LangGraph state and workflow definition
        ├── __init__.py
        ├── builder.py
        └── state.py
