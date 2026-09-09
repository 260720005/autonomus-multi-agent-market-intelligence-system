from backend.agents.trend_agent import trend_research


task = """
Identify the major emerging trends in Agentic AI
that could shape the market during 2026 and beyond.
"""


result = trend_research(task)


print("\nTREND FINDING\n")

print("Task:")
print(result.task)

print("\nSummary:")
print(result.summary)

print("\nTrends:")

for trend in result.trends:
    print("-", trend)

print("\nSignals:")

for signal in result.signals:
    print("-", signal)

print("\nImpact:")

for impact in result.impact:
    print("-", impact)

print("\nTime Horizon:")

for horizon in result.time_horizon:
    print("-", horizon)

print("\nSources:")

for source in result.sources:
    print("-", source)