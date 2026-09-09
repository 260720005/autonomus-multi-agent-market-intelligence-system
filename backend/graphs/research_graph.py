from langgraph.graph import StateGraph, START, END
from typing import Literal #Function kya kya Exact Values return kr sakta hai

from backend.models.state import ResearchState
from backend.agents.planner import create_research_plan
from backend.agents.market_agent import market_research
from backend.agents.company_agent import company_research
from backend.agents.trend_agent import trend_research
from backend.agents.critic_agent import evaluate_research
from backend.models.validated import ValidatedFinding
from backend.models.aggregated import AggregatedEvidence
from backend.agents.analyst_agent import analyze_evidence
from backend.agents.report_generator import generate_report
from backend.rag.memory import store_report_in_memory
from backend.rag.retriever import retrieve_relevant_chunks

def rag_retriever_node(state: ResearchState):
    """Retrieve relevant information from previous reports."""

    print("\n🔎 Searching RAG memory...")
    query = state["user_query"]

    rag_context = retrieve_relevant_chunks(
        query,
        top_k=3
    )

    print(f"🧠 Retrieved {len(rag_context)} relevant chunks from memory.")

    for i, chunk in enumerate(rag_context, start=1):
        print(f"\n--- Retrieved Chunk {i} ---")
        print(chunk)

    return {
        "rag_context": rag_context
    }

def planner_node(state: ResearchState):
    """Create a research plan from the user's query."""
    plan = create_research_plan(
        state["user_query"],
        state["rag_context"]
    )
    return{
        "research_plan": plan
    }

def market_node(state: ResearchState):
    """Execute market research task."""

    findings = []

    for i , task in enumerate(
        state["research_plan"].market_tasks,
        start = 1
    ):

        print(f"\n📊 Market Agent researching: {task}")

        try:
            finding = market_research(task)
            findings.append(finding)

            print(f"✅ Market Task {i} completed.")
        except Exception as e:
            print(f"❌ Market Task {i} failed: {e}")

    return {
        "market_results": findings
    }

def company_node(state: ResearchState):
    """Execute company research tasks."""

    findings = []

    for i, task in enumerate(
        state["research_plan"].company_tasks,
        start=1
    ):
        print(f"\n🏢 Company Agent researching: {task}")

        try:
            finding = company_research(task)
            findings.append(finding)

            print(f"✅ Company Task {i} completed.")

        except Exception as e:
            print(f"❌ Company Task {i} failed: {e}")

    return {
        "company_results": findings
    }

def trend_node(state: ResearchState):
    """Execute trend research tasks."""

    findings = []

    for i, task in enumerate(
        state["research_plan"].trend_tasks,
        start=1
    ):
        print(f"\n📈 Trend Agent researching: {task}")

        try:
            finding = trend_research(task)
            findings.append(finding)

            print(f"✅ Trend Task {i} completed.")

        except Exception as e:
            print(f"❌ Trend Task {i} failed: {e}")

    return {
        "trend_results": findings
    }

def prepare_validation_node(state: ResearchState):
    findings=[]

    # Market findings
    for finding in state["market_results"]:
        findings.append({
            "task": finding.task,
            "type": "market",
            "finding": finding
        })

    # Company findings
    for finding in state["company_results"]:
        findings.append({
            "task": finding.task,
            "type": "company",
            "finding": finding
        })

    # Trend findings
    for finding in state["trend_results"]:
        findings.append({
            "task": finding.task,
            "type": "trend",
            "finding": finding
        })

    return {
        "findings_to_validate": findings
    }


def critic_node(state: ResearchState):
    """Validate all research findings."""

    critic_results = []
    validated_findings = []
    research_queue = []

    for item in state["findings_to_validate"]:
        task = item["task"]
        research_type = item["type"]
        finding = item["finding"]

        print(
            f"\n🔍 Critic validating "
            f"{research_type} finding: {task}"
        )
        try:
            result = evaluate_research(
                task,
                finding
            )

            critic_results.append(result)

            if result.valid:
                validated_findings.append(
                    ValidatedFinding(
                        task=task,
                        type=research_type,
                        finding=finding,
                        critic=result
                    )
                )

            if not result.valid:
                research_queue.append({
                    "task": task,
                    "type": research_type
                })
            print(
                f"✅ {research_type.title()} finding validated | "
                f"Valid: {result.valid} | "
                f"Relevance: {result.relevance_score}/10 | "
                f"Evidence: {result.evidence_score}/10"
            )
        except Exception as e:
            print(
                f"❌ {research_type.title()} validation failed: {e}"
            )
    return {
        "critic_results": critic_results,
        "validated_findings": validated_findings,
        "research_queue": research_queue
    }

def evidence_aggregator_node(state: ResearchState):
    """Organize validated findings into structured evidence."""

    market_evidence = []
    company_evidence = []
    trend_evidence = []

    for finding in state["validated_findings"]:

        if finding.type == "market":
            market_evidence.append(finding)

        elif finding.type == "company":
            company_evidence.append(finding)

        elif finding.type == "trend":
            trend_evidence.append(finding)

    aggregated_evidence = AggregatedEvidence(
        market_evidence=market_evidence,
        company_evidence=company_evidence,
        trend_evidence=trend_evidence
    )

    print("\n Evidence Aggregation Completed")
    print(f"Market Evidence: {len(market_evidence)}")
    print(f"Company Evidence: {len(company_evidence)}")
    print(f"Trend Evidence: {len(trend_evidence)}")

    return{
        "aggregated_evidence": aggregated_evidence
    }

def analyst_node(state: ResearchState):
    """Analyze aggregated evidence and generate strategic insights."""

    aggregated_evidence = state["aggregated_evidence"]

    if aggregated_evidence is None:
        raise ValueError("Aggregated evidence is not available.")

    print("\n🧠 Starting Analyst Agent...")

    result = analyze_evidence(aggregated_evidence , state["rag_context"])
    print("✅ Analyst analysis completed.")

    return {
        "analyst_result": result
    }

def report_generator_node(state: ResearchState):
    """generate the final market intelligence report."""

    analyst_result = state["analyst_result"]

    if analyst_result is None:
        raise ValueError("Analyst result is not Available.")

    print("\n📝 Starting Report Generator Agent...")

    result = generate_report(analyst_result)

    print("✅ Final report generated.")

    report_id = store_report_in_memory(result)

    print(f"🧠 Report stored in RAG memory.  ID: {report_id}")

    return {
        "report_result": result
        }

def re_research_node(state: ResearchState):
    """Re-research findings that failed validation."""

    new_findings = []

    research_attempts = state["research_attempts"].copy()

    for item in state["research_queue"]:

        task = item["task"]
        research_type = item["type"]

        current_attempts = research_attempts.get(task, 0)

        if current_attempts >= 1:
            print(
                f"🛑 Max re-research attempts reached: {task}"
            )
            continue

        research_attempts[task] = current_attempts + 1

        print(
            f"\n🔄 Re-researching: {task} "
            f"(Attempt {research_attempts[task]}/1)"
        )

        try:

            if research_type == "market":

                finding = market_research(task)
            elif research_type == "company":

                finding = company_research(task)
            elif research_type == "trend":

                finding = trend_research(task)
            else:
                print(
                    f"❌ Unknown research type: {research_type}"
                )
                continue

            new_findings.append({
                "task": task,
                "type": research_type,
                "finding": finding
            })

            print(
                f"✅ {research_type.title()} "
                f"re-research completed."
            )

        except Exception as e:
            print(f"❌ Re-research failed: {e}")

    return {
        "findings_to_validate": new_findings,
        "research_queue": [],
        "research_attempts": research_attempts
    }

def route_after_critic(state: ResearchState) -> Literal["re_research", "aggregate"]:
    """Decides whether the failed research should be repeated or not."""

    if state["research_queue"]:
        return "re_research"

    return "aggregate"

## Create the graph
graph_builder = StateGraph(ResearchState)

## Add nodes 
graph_builder.add_node("rag_retriever", rag_retriever_node)
graph_builder.add_node("planner", planner_node)
graph_builder.add_node("market", market_node)
graph_builder.add_node("company", company_node)
graph_builder.add_node("trend", trend_node)
graph_builder.add_node("prepare_validation", prepare_validation_node)
graph_builder.add_node("critic", critic_node)
graph_builder.add_node("re_research", re_research_node)
graph_builder.add_node("evidence_aggregator", evidence_aggregator_node)
graph_builder.add_node("analyst", analyst_node)
graph_builder.add_node("report_generator", report_generator_node)

# Planner → specialized agents
graph_builder.add_edge(START, "rag_retriever")
graph_builder.add_edge("rag_retriever", "planner")

graph_builder.add_edge("planner", "market")
graph_builder.add_edge("planner", "company")
graph_builder.add_edge("planner", "trend")


# Specialized agents → END
graph_builder.add_edge("market", "prepare_validation")
graph_builder.add_edge("company", "prepare_validation")
graph_builder.add_edge("trend", "prepare_validation")

graph_builder.add_edge("prepare_validation", "critic")

graph_builder.add_conditional_edges(
    "critic",
    route_after_critic,
    {
        "re_research": "re_research",
        "aggregate": "evidence_aggregator"
    } # Ye mapping hori hai 
)

graph_builder.add_edge("re_research", "critic")
graph_builder.add_edge("evidence_aggregator", "analyst")
graph_builder.add_edge("analyst", "report_generator")
graph_builder.add_edge("report_generator", END)



#Compile the graph
research_graph = graph_builder.compile()

if __name__ == "__main__":

    # Test the graph
    initial_state = {
        "user_query": "Analyze the electric vehicle market in India in 2025.",
        "research_plan":None,
        "research_results":[],
        "market_results":[],
        "company_results": [],
        "trend_results": [],
        "critic_results": [],
        "validated_findings": [],
        "aggregated_evidence": None,
        "analyst_result": None,
        "report_result": None,
        "rag_context": [],
        "research_queue": [],
        "findings_to_validate": [],
        "research_attempts": {}
    }

    result = research_graph.invoke(initial_state)

    print("\n========== MARKET RESULTS ==========")

    for i, finding in enumerate(result["market_results"], start=1):

        print(f"\n--- Market Finding {i} ---")

        print("Task:")
        print(finding.task)

        print("\nSummary:")
        print(finding.summary)

        print("\nKey Points:")

        for point in finding.key_points:
            print("-", point)

        print("\nMetrics:")

        for metric in finding.metrics:
            print("-", metric)

        print("\nGeography:")

        for region in finding.geography:
            print("-", region)

        print("\nSources:")

        for source in finding.sources:
            print("-", source)


    print("\n========== COMPANY RESULTS ==========")

    for i, finding in enumerate(result["company_results"], start=1):

        print(f"\n--- Company Finding {i} ---")

        print("Task:")
        print(finding.task)

        print("\nSummary:")
        print(finding.summary)

        print("\nCompanies:")

        for company in finding.companies:
            print("-", company)

        print("\nProducts:")

        for product in finding.products:
            print("-", product)

        print("\nKey Points:")

        for point in finding.key_points:
            print("-", point)

        print("\nSources:")

        for source in finding.sources:
            print("-", source)


    print("\n========== TREND RESULTS ==========")

    for i, finding in enumerate(result["trend_results"], start=1):

        print(f"\n--- Trend Finding {i} ---")

        print("Task:")
        print(finding.task)

        print("\nSummary:")
        print(finding.summary)

        print("\nTrends:")

        for trend in finding.trends:
            print("-", trend)

        print("\nSignals:")

        for signal in finding.signals:
            print("-", signal)

        print("\nImpact:")

        for impact in finding.impact:
            print("-", impact)

        print("\nTime Horizon:")

        for horizon in finding.time_horizon:
            print("-", horizon)

        print("\nSources:")

        for source in finding.sources:
            print("-", source)

    print("\n========== CRITIC RESULTS ==========")

    for i, critic_result in enumerate(result["critic_results"], start=1):

        print(f"\n--- Critic Result {i} ---")

        print("Valid:")
        print(critic_result.valid)

        print("Relevance Score:")
        print(f"{critic_result.relevance_score}/10")

        print("Evidence Score:")
        print(f"{critic_result.evidence_score}/10")

        print("Issues:")
        for issue in critic_result.issues:
            print("-", issue)

        print("Reason:")
        print(critic_result.reason)

        print("Needs Research:")
        print(critic_result.needs_research)

    print("\n========== AGGREGATED EVIDENCE ==========")

    aggregated = result["aggregated_evidence"]
    print("Aggregated:", aggregated)

    print("\nMarket Evidence:")

    for item in aggregated.market_evidence:
        print("-", item.task)

    print("\nCompany Evidence:")

    for item in aggregated.company_evidence:
        print("-", item.task)

    print("\nTrend Evidence:")

    for item in aggregated.trend_evidence:
        print("-", item.task)

    print("\n========== ANALYST RESULT ==========")

    analyst = result["analyst_result"]

    print("\nExecutive Summary:")
    print(analyst.executive_summary)

    print("\nMarket Insights:")
    for insight in analyst.market_insights:
        print("-", insight)

    print("\nCompany Insights:")
    for insight in analyst.company_insights:
        print("-", insight)

    print("\nTrend Insights:")
    for insight in analyst.trend_insights:
        print("-", insight)

    print("\nGrowth Drivers:")
    for driver in analyst.growth_drivers:
        print("-", driver)

    print("\nRisks:")
    for risk in analyst.risks:
        print("-", risk)

    print("\nOpportunities:")
    for opportunity in analyst.opportunities:
        print("-", opportunity)

    print("\nStrategic Outlook:")
    print(analyst.strategic_outlook)

    print("\n========== FINAL MARKET INTELLIGENCE REPORT ==========")

    report = result["report_result"]

    print("\nTitle:")
    print(report.title)

    print("\nExecutive Summary:")
    print(report.executive_summary)

    print("\nMarket Analysis:")
    for item in report.market_analysis:
        print("-", item)

    print("\nCompetitive Landscape:")
    for item in report.competitive_landscape:
        print("-", item)

    print("\nTrend Analysis:")
    for item in report.trend_analysis:
        print("-", item)

    print("\nGrowth Drivers:")
    for item in report.growth_drivers:
        print("-", item)

    print("\nRisks:")
    for item in report.risks:
        print("-", item)

    print("\nOpportunities:")
    for item in report.opportunities:
        print("-", item)

    print("\nStrategic Outlook:")
    print(report.strategic_outlook)

    print("\n======================================================")