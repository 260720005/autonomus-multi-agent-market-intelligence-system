from langchain_groq import ChatGroq

from backend.config.config import GROQ_API_KEY
from backend.models.company import CompanyFinding
from backend.tools.web_search import web_search
from backend.utils.retry import retry_with_backoff

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY
)

company_analyzer = llm.with_structured_output(
    CompanyFinding,
    method="function_calling"
)

@retry_with_backoff(max_retries=4, initial_delay=5)
def invoke_company_analyzer(prompt):
    return company_analyzer.invoke(prompt)


def company_research(task: str) -> CompanyFinding:
    """
    Perform specialized company and competitive research.
    """

    search_results = web_search.invoke({
        "query": task
    })

    prompt = f"""
You are the Company Research Agent in an autonomous
multi-agent market intelligence system.

Your specialization is COMPANY AND COMPETITIVE INTELLIGENCE.

Research task:
{task}

Web search results:
{search_results}

Analyze the provided sources and extract reliable
company-related intelligence.

Focus on:

1. Major companies
2. Products and platforms
3. Competitive positioning
4. Product capabilities
5. Funding and investments
6. Partnerships
7. Enterprise deployments
8. Target industries
9. Competitive strengths
10. Relevant competitive differences

Rules:

- Use only information supported by the provided search results.
- Do not invent companies, products, customers, or numbers.
- Distinguish companies from their products.
- Prefer recent and authoritative information.
- Keep factual claims tied to the provided sources.

- Treat multiple sources reporting the same underlying company
  claim as corroborating evidence, not as separate independent facts.
- Prefer the strongest and most directly relevant source
  when multiple sources support the same claim.
- Identify conflicting company claims instead of silently
  combining them.

- For funding, valuation, revenue, customer, adoption,
  deployment, or other quantitative claims:
  - Preserve the year or date when available.
  - Preserve the relevant company or business scope.
  - Do not present historical figures as current figures.
  - Do not present forecasts or estimates as confirmed facts.
  - Include the supporting source.

- Clearly distinguish:
  - Company claims
  - Independent evidence
  - Analyst or media interpretation
  - Future plans or announcements

- If the available sources do not provide enough evidence
  for an important claim, say so rather than filling the gap.

- Include URLs supporting the findings.
- Return the result using the required CompanyFinding structure.
"""

    result = invoke_company_analyzer(prompt)

    return result