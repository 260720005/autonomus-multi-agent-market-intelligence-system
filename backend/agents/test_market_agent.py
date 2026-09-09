from backend.agents.market_agent import market_research

task = """
Analyze the Agentic AI market size, growth rate,
and forecast for 2026.
"""

result = market_research(task)


print("\nMARKET FINDING\n")

print("Task:")
print(result.task)

print("\nSummary:")
print(result.summary)

print("\nKey Points:")
for point in result.key_points:
    print("-", point)

print("\nMetrics:")
for metric in result.metrics:
    print("-", metric)

print("\nGeography:")
for region in result.geography:
    print("-", region)

print("\nSources:")
for source in result.sources:
    print("-", source)