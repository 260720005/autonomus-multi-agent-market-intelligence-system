from backend.agents.research_agent import research_task

task = " Identify the major comapnies in the Agentic Ai market in 2026?"

result = research_task(task)

print("\nRESEARCH FINDING\n")
print("Task:")
print(result.task)

print("\nSummary:")
print(result.summary)

print("\nKey Points:")
for point in result.key_points:
    print("-", point)

print("\nSources:")
for source in result.sources:
    print("-", source)
