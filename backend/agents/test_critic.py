from backend.agents.critic_agent import evaluate_research

task = "Analyze the geographic distribution of the Agentic AI market."

finding = """
Summary:
The United States currently represents a major market
for Agentic AI adoption, while Europe and Asia-Pacific
are also showing increasing enterprise adoption.

Key Points:
- US has strong enterprise AI adoption.
- Europe is increasing investment in AI.
- Asia-Pacific is emerging as a significant region.

Sources:
- https://example.com/agentic-ai-market
"""


result = evaluate_research(task, finding)

print("\n========== CRITIC RESULT ==========")

print("\nValid:")
print(result.valid)

print("\nRelevance Score:")
print(result.relevance_score)

print("\nEvidence Score:")
print(result.evidence_score)

print("\nIssues:")
for issue in result.issues:
    print("-", issue)

print("\nReason:")
print(result.reason)

print("\nNeeds Research:")
print(result.needs_research)