from langchain_groq import ChatGroq

from backend.config.config import GROQ_API_KEY
from backend.models.analyst import AnalystResult
from backend.models.report import ReportResult
from backend.utils.retry import retry_with_backoff


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY
)


ReportGenerator = llm.with_structured_output(
    ReportResult,
    method="function_calling"
)


@retry_with_backoff(max_retries=4, initial_delay=10)
def invoke_report_generator(prompt):
    return ReportGenerator.invoke(prompt)


def generate_report(analysis: AnalystResult) -> ReportResult:
    """
    Generate a professional market intelligence report
    from the strategic analysis produced by the Analyst Agent.
    """

    prompt = f"""
You are the Report Generator Agent in an autonomous
multi-agent market intelligence system.

Your job is to transform the strategic analysis produced
by the Analyst Agent into a clear, professional,
decision-oriented market intelligence report.

Do not perform new research.
Do not invent facts.
Do not introduce information that is not present
in the provided analyst analysis.

ANALYST ANALYSIS:

Executive Summary:
{analysis.executive_summary}

Market Insights:
{analysis.market_insights}

Company Insights:
{analysis.company_insights}

Trend Insights:
{analysis.trend_insights}

Growth Drivers:
{analysis.growth_drivers}

Risks:
{analysis.risks}

Opportunities:
{analysis.opportunities}

Strategic Outlook:
{analysis.strategic_outlook}

Create the final report with the following sections:

1. TITLE
- Create a concise and professional title for the report.

2. EXECUTIVE SUMMARY
- Present the overall market assessment clearly.
- Preserve important uncertainty mentioned by the analyst.

3. MARKET ANALYSIS
- Present the most important market insights.
- Include quantitative information only when provided
  by the analyst.
- Do not change the meaning of reported figures.

4. COMPETITIVE LANDSCAPE
- Present important company and competitive insights.
- If company insights are unavailable, return an empty list.
- Never invent companies or competitive information.

5. TREND ANALYSIS
- Present the most important current and emerging trends.
- Focus on evidence-supported trends.

6. GROWTH DRIVERS
- Present the major factors supporting market growth.

7. RISKS
- Present important risks, barriers and uncertainties.

8. OPPORTUNITIES
- Present meaningful business and market opportunities.

9. STRATEGIC OUTLOOK
- Present the analyst's forward-looking assessment.
- Do not introduce new predictions.

IMPORTANT RULES:

- Use only the information provided in the analyst analysis.
- Do not perform web searches.
- Do not invent statistics, companies, products,
  forecasts or market information.
- Preserve important uncertainty and conflicting estimates.
- Do not convert uncertain information into definite facts.
- Do not introduce new conclusions that are not supported
  by the analyst analysis.
- Preserve important numbers, dates, geographies,
  and time periods from the analyst analysis.
- Clearly preserve the distinction between evidence-supported
  insights and forward-looking interpretation.
- If the analyst identifies insufficient evidence for a topic,
  preserve that limitation in the final report.
- Do not strengthen cautious or qualified statements into
  definitive claims.
- Avoid unnecessary repetition.
- Keep the report concise and professional.

Return the result using the required ReportResult structure.
"""

    result = invoke_report_generator(prompt)

    return result