from backend.agents.planner import create_research_plan

query = "Analyze the Agentic AI market in 2026."

result = create_research_plan(query)

print("\nMARKET TASKS:\n")

for task in result.market_tasks:
    print("-", task)

print("\nCOMPANY TASKS:\n")

for task in result.company_tasks:
    print("-", task)


print("\nTREND TASKS:\n")

for task in result.trend_tasks:
    print("-", task)