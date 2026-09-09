from langchain_groq import ChatGroq
from backend.config.config import GROQ_API_KEY
from backend.models.research import ResearchFinding
from backend.tools.web_search import web_search

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=GROQ_API_KEY
)

research_analyzer = llm.with_structured_output(
    ResearchFinding,
    method="function_calling"
)

def research_task(task: str) -> ResearchFinding:
    """
    Research a single task using web search
    and summarize the findings.
    """

    search_results = web_search.invoke({
        "query": task
    })

    prompt = f"""
You are a Research Agent in an autonomous market intelligence system.

Research task:
{task}

Below are web search results collected for this task:

{search_results}

Your job is to produce a structured research finding.

Requirements:

1. Summarize only information relevant to the research task.
2. Extract important factual findings from the search results.
3. Do not invent information.
4. Use only the provided search results as evidence.
5. Include the URLs of the sources that support your findings.
6. Keep the summary concise.
7. Return the answer using the required ResearchFinding structure.
"""

    result = research_analyzer.invoke(prompt)

    return result