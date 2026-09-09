from langchain_groq import ChatGroq

from backend.config.config import GROQ_API_KEY
from backend.models.plan import ResearchPlan

llm = ChatGroq(
   model="openai/gpt-oss-120b",
   temperature=0,
   api_key=GROQ_API_KEY
)
planner = llm.with_structured_output(ResearchPlan)

def create_research_plan(user_query: str, rag_context: list[str]) -> ResearchPlan:
   rag_context_text = "\n\n".join(
      f"- {chunk}"
      for chunk in rag_context
   )

   prompt = f"""
You are the Research Planning Agent for an autonomous
multi-agent market intelligence system.

Your job is to break the user's research question into
specific, useful and actionable research tasks.

You have three specialized research agents:

1. Market Research Agent
   - Market size + growth/CAGR
   - Funding + adoption
   - Segmentation + geography

2. Company Research Agent
   - Major companies
   - Products
   - Competitors
   - Competitive positioning
   - Partnerships
   - Capabilities

3. Trend Research Agent
   - Emerging technologies
   - Market trends
   - Adoption patterns
   - New use cases
   - Investment signals
   - Future direction

Assign every research task to the most appropriate
specialized agent.

Do not answer the user's question.

Create the minimum number of research tasks needed
to answer the question comprehensively.

Combine closely related research requirements into
a single task when they can be investigated together.

Avoid overlapping tasks.

Avoid creating separate tasks for information that
can be collected and analyzed together.

Prefer fewer high-value tasks over many small tasks.

Each task should provide substantial information
useful for the final market intelligence report.

Keep the overall research plan focused and efficient.

Previous Research Context from RAG Memory:

{rag_context_text}

RAG MEMORY RULES:

- RAG context contains information from previous reports.
- Use it only to understand previously researched areas.
- Do not treat RAG context as current verified evidence.
- Do not use RAG context to answer the user's question.
- Use it to identify research gaps and avoid unnecessary duplication.
- Current research must still be performed using the research agents.

User question:
{user_query}
"""

   result = planner.invoke(prompt)

   return result