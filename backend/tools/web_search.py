from langchain_tavily import TavilySearch
from backend.config.config import TAVILY_API_KEY

web_search = TavilySearch(
    max_results = 5,
    topic = "general",
    search_depth = "advanced",
    tavily_api_key = TAVILY_API_KEY
)