from langchain_groq import ChatGroq

from backend.config.config import GROQ_API_KEY
from backend.models.trend import TrendFinding
from backend.tools.web_search import web_search
from backend.utils.retry import retry_with_backoff


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY
)

trend_analyzer = llm.with_structured_output(
    TrendFinding,
    method="function_calling"
)

@retry_with_backoff(max_retries=4, initial_delay=5)
def invoke_trend_analyzer(prompt):
    return trend_analyzer.invoke(prompt)


def trend_research(task: str) -> TrendFinding:
    """
    Perform specialized trend and emerging-signal research.
    """

    search_results = web_search.invoke({
        "query": task
    })

    prompt = f"""
You are the Trend Research Agent in an autonomous
multi-agent market intelligence system.

Your specialization is TREND AND EMERGING-SIGNAL INTELLIGENCE.

Research task:
{task}

Web search results:
{search_results}

Analyze the provided sources and identify meaningful
current and emerging trends.

Focus on:

1. Emerging technologies
2. Agent architectures
3. Enterprise adoption patterns
4. Developer ecosystem changes
5. Investment and funding signals
6. New use cases
7. Governance and regulation
8. Infrastructure changes
9. Competitive shifts
10. Future market direction

Rules:

- Use only information supported by the provided search results.
- Do not invent trends or evidence.
- Distinguish current trends from predictions.
- Distinguish evidence from speculation.
- Identify concrete signals supporting important trends.
- Explain potential market or business impact.
- Include the relevant time horizon.

- Treat multiple sources reporting the same underlying trend
  as corroborating evidence, not as separate independent facts.
- Prefer the strongest and most directly relevant source
  when multiple sources support the same trend.
- Identify conflicting trend signals instead of silently
  combining them.

- Clearly distinguish:
  - Observed current trends
  - Emerging signals
  - Company announcements
  - Analyst or media predictions
  - Speculative future scenarios

- For adoption, investment, funding, market growth, or other
  quantitative claims:
  - Preserve the year or date when available.
  - Preserve the relevant geography, industry, or population scope.
  - Do not present historical figures as current figures.
  - Do not present forecasts or predictions as confirmed facts.
  - Include the supporting source.

- A trend should be supported by concrete evidence such as
  adoption data, investment activity, product launches,
  enterprise deployments, regulatory developments, or
  repeated signals from credible sources.

- If the available sources do not provide enough evidence
  to establish an important trend, say so rather than
  presenting speculation as fact.

- Include URLs supporting the findings.
- Return the result using the required TrendFinding structure.
"""

    result = invoke_trend_analyzer(prompt)

    return result