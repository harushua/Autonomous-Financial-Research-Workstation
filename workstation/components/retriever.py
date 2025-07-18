import os
from dotenv import load_dotenv

# LangChain and supporting libraries
from langchain_core.documents import Document
from langchain_tavily import TavilySearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain_openai import OpenAIEmbeddings
from langchain.retrievers import EnsembleRetriever

# Native SDKs
from firecrawl import FirecrawlApp

# Load environment variables from .env file
load_dotenv()

def build_hybrid_retriever(topic: str):
    """
    Searches for a topic, scrapes the content, and builds a hybrid search retriever.

    This function implements the "Qualitative Data Arm" of our research workstation.

    Args:
        topic: The topic to research (e.g., "NVIDIA's performance in the AI chip market").

    Returns:
        An EnsembleRetriever object ready to be used in a RAG chain, or None if an error occurs.
    """
    # --- 1. Discover URLs with Tavily ---
    print(f"🔬 Step 1: Searching for '{topic}' with Tavily...")
    tavily_tool = TavilySearch(max_results=3, topic="finance", search_depth="advanced")
    try:
        results = tavily_tool.invoke(topic)
        urls = [result['url'] for result in results['results']]
        print(f"   ✅ Found URLs: {urls}")
    except Exception as e:
        print(f"   ❌ Error during Tavily search: {e}")
        return None

    # --- 2. Scrape Content with Firecrawl ---
    print("\n🔥 Step 2: Scraping content with Firecrawl...")
    all_docs = []
    firecrawl_app = FirecrawlApp()

    for url in urls:
        try:
            scraped_data = firecrawl_app.scrape_url(url=url,formats=['markdown'])
            if scraped_data and scraped_data.markdown:
                doc = Document(
                    page_content=scraped_data.markdown,
                    metadata={'source': url}
                )
                all_docs.append(doc)
                print(f"   ✅ Successfully scraped: {url}")
            else:
                print(f"   ⚠️ No markdown content found for: {url}")
        except Exception as e:
            print(f"   ❌ Could not scrape {url}: {e}")

    if not all_docs:
        print("\nNo documents were successfully scraped. Exiting.")
        return None

    # --- 3. Split and Index Documents (Hybrid Search) ---
    print(f"\n📚 Step 3: Indexing content from {len(all_docs)} documents for hybrid search...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    chunks = text_splitter.split_documents(all_docs)

    # a) Create BM25 retriever for keyword search
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 5

    # b) Create FAISS vector store for semantic search
    embedding_model = OpenAIEmbeddings()
    faiss_vectorstore = FAISS.from_documents(chunks, embedding_model)
    faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k": 5})

    # c) Create the Ensemble Retriever
    ensemble_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, faiss_retriever],
        weights=[0.5, 0.5],
        search_type="mmr"
    )
    print("   ✅ Hybrid retriever created successfully.")
    return ensemble_retriever
