from langchain_groq import ChatGroq

from backend.config.config import GROQ_API_KEY
from backend.models.market import MarketFinding
from backend.tools.web_search import web_search
from backend.utils.retry import retry_with_backoff

llm = ChatGroq(
    model= "openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY
)

market_analyzer = llm.with_structured_output(
    MarketFinding,
    method = "function_calling"
)

@retry_with_backoff(max_retries=4, initial_delay=5)
def invoke_market_analyzer(prompt):
    return market_analyzer.invoke(prompt)


def market_research(task:str) -> MarketFinding:
    """
    Perform specialized market research for a single task.
    """

    search_results=web_search.invoke({
        "query": task
    })

    prompt = f"""
You are the Market Research Agent in an autonomous
multi-agent market intelligence system.

Your specialization is MARKET INTELLIGENCE.

Research task:
{task}

Web search results:
{search_results}

Your job is to analyze the provided search results
and extract reliable market intelligence.

Focus on:

1. Market size
2. Growth rates and CAGR
3. Forecasts
4. TAM, SAM and SOM when available
5. Funding and investment
6. Enterprise adoption
7. Market segmentation
8. Regional market dynamics
9. Market drivers
10. Market barriers

Rules:

- Use only information supported by the provided search results.
- Do not invent numbers.
- Preserve the year associated with every quantitative claim.
- Preserve the geography associated with every quantitative claim.
- Clearly distinguish historical data from forecasts.
- If reliable quantitative data is unavailable, say so.
- Extract important quantitative metrics separately.

- Treat multiple sources reporting the same underlying claim
  as corroborating evidence, not as separate independent facts.
- Prefer the strongest and most directly relevant source
  when multiple sources support the same claim.
- Identify conflicting quantitative estimates instead of
  silently combining them.

- Include the URLs of sources supporting the findings.
- Return the result using the required MarketFinding structure.
"""

    result = invoke_market_analyzer(prompt)

    return result