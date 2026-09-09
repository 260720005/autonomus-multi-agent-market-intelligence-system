from langchain_groq import ChatGroq

from backend.config.config import GROQ_API_KEY
from backend.models.aggregated import AggregatedEvidence
from backend.models.analyst import AnalystResult
from backend.utils.retry import retry_with_backoff

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY
)

Analyst = llm.with_structured_output(
    AnalystResult,
    method = "function_calling"
)
@retry_with_backoff(max_retries=4, initial_delay=10)
def invoke_analyst(prompt):
    return Analyst.invoke(prompt)

def analyze_evidence(evidence: AggregatedEvidence, rag_context: list[str]) -> AnalystResult:
    """
    Analyze validated and aggregated research evidence
    and produce strategic market insights.

    """
    market_evidence = [
        {
            "task": item.task,
            "finding": item.finding
        }
        for item in evidence.market_evidence
    ]

    company_evidence = [
        {
            "task": item.task,
            "finding": item.finding
        }
        for item in evidence.company_evidence
    ]

    trend_evidence = [
        {
            "task": item.task,
            "finding": item.finding
        }
        for item in evidence.trend_evidence
    ]
    rag_context_text = "\n\n".join(
        f"- {chunk}"
        for chunk in rag_context
    )

    prompt = f"""
You are the Analyst Agent in an autonomous
multi-agent market intelligence system.

Your job is to analyze validated research evidence
collected by multiple specialized research agents.

You must derive meaningful strategic insights from
the provided evidence.

Do not perform new research.
Do not invent facts.
Use only the information contained in the evidence.

RAG MEMORY RULES:

- RAG context contains information from previous reports.
- Use RAG context only as historical or contextual information.
- Do not treat RAG context as newly validated evidence.
- Prefer current validated evidence over information from RAG memory.
- If RAG context conflicts with current validated evidence,
  prefer the current validated evidence.
- Do not introduce a fact from RAG memory as a current fact
  unless it is also supported by the current validated evidence.

CURRENT EVIDENCE SAFETY RULES:

- Current validated evidence is the only authoritative evidence
  for current market conclusions.

- RAG memory must never substitute for missing current evidence.

- If a topic has no current validated evidence, explicitly state
  that the available evidence is insufficient.

- Do not use historical RAG information to create current
  market sizes, growth rates, company claims, adoption metrics,
  forecasts, or other factual conclusions.

- RAG information may be mentioned only when clearly identified
  as historical context.

- If current validated evidence is empty or insufficient,
  do not infer or reconstruct the missing information from RAG memory.

PREVIOUS REPORT CONTEXT FROM RAG MEMORY:

{rag_context_text}

AGGREGATED EVIDENCE:

Market Evidence:
{market_evidence}

Company Evidence:
{company_evidence}

Trend Evidence:
{trend_evidence}

Analyze the evidence and provide:

1. EXECUTIVE SUMMARY
- Give a concise overall assessment of the market.

2. MARKET INSIGHTS
- Identify the most important market-level findings.
- Focus on market size, segmentation, growth and geography
  when supported by the evidence.

3. COMPANY INSIGHTS
- Identify important competitive or company-level patterns.
- If company evidence is unavailable, do not invent company insights.

4. TREND INSIGHTS
- Identify the most important current and emerging trends.

5. GROWTH DRIVERS
- Identify the major factors driving market growth.

6. RISKS
- Identify important risks, barriers and uncertainties
  supported by the evidence.

7. OPPORTUNITIES
- Identify potential business or market opportunities
  supported by the evidence.

8. STRATEGIC OUTLOOK
- Provide a forward-looking assessment based only on
  the available evidence.

Important rules:

- Do not invent statistics, companies, market sizes,
  forecasts or other facts.
- Do not perform additional web searches.
- Clearly distinguish evidence-supported conclusions
  from uncertainty.
- Do not treat conflicting estimates as a single fact.
- When evidence is contradictory, mention the uncertainty.
- Keep the analysis focused on the original research task.
- Prefer concise, actionable insights over repetition.

- Clearly distinguish directly supported evidence
  from analytical inference.

- When making an inference, base it on one or more
  specific pieces of current validated evidence.

- Do not turn a weak signal into a definitive conclusion.

- Preserve important quantitative values, dates,
  geographies, and time periods from the validated evidence.

- When evidence is insufficient for a strategic conclusion,
  explicitly state the limitation instead of filling the gap.

Return the result using the required AnalystResult structure.
"""

    result = invoke_analyst(prompt)
    return result

