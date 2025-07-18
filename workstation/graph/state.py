from typing import TypedDict, List, Optional
from langchain.retrievers import EnsembleRetriever

class ResearchState(TypedDict):
    """
    Represents the state of our financial research graph.
    """
    topic: str
    ticker: str
    qualitative_data_retriever: Optional[EnsembleRetriever]
    quantitative_data: Optional[dict]
    analysis: str
    chart_data: Optional[List[dict]]
    chart_image_paths: List[str]
    report_path: str # <-- Changed from final_report to store the path

