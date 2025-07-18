import os
from dotenv import load_dotenv

# Import the Polygon Toolkit and API Wrapper
from langchain_community.agent_toolkits.polygon.toolkit import PolygonToolkit
from langchain_community.utilities.polygon import PolygonAPIWrapper

# Load environment variables from .env file
load_dotenv()

def get_financial_data(ticker: str):
    """
    Fetches financial data and news for a given stock ticker using the Polygon API.

    This function implements the "Quantitative Data Arm" of our research workstation.

    Args:
        ticker: The stock ticker symbol (e.g., "NVDA").

    Returns:
        A dictionary containing structured financial data and news, or None if an error occurs.
    """
    print(f"\n📈 Step 1 (Quant): Fetching financial data for '{ticker}'...")

    try:
        # Initialize the Polygon API wrapper and toolkit
        polygon_api = PolygonAPIWrapper()
        toolkit = PolygonToolkit.from_polygon_api_wrapper(polygon_api)

        # The toolkit provides a list of tools. We can select the ones we need.
        tools_map = {tool.name: tool for tool in toolkit.get_tools()}
        
        financials_tool = tools_map.get("polygon_financials")
        news_tool = tools_map.get("polygon_ticker_news")

        if not financials_tool or not news_tool:
            print("   ❌ Required Polygon tools (financials, news) not found.")
            return None

        # Fetch financials and news data
        # Note: The 'invoke' method on these tools expects a dictionary
        financials_data = financials_tool.invoke({"query": ticker})
        news_data = news_tool.invoke({"query": ticker})
        
        print(f"   ✅ Successfully fetched financial data and news for {ticker}.")

        return {
            "financials": financials_data,
            "news": news_data
        }

    except Exception as e:
        print(f"   ❌ An error occurred while fetching Polygon data: {e}")
        return None

