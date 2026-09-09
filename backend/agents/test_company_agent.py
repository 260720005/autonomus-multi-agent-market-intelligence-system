from backend.agents.company_agent import company_research


task = """
Identify the major companies competing in the
Agentic AI market in 2026 and their key products.
"""


result = company_research(task)


print("\nCOMPANY FINDING\n")

print("Task:")
print(result.task)

print("\nSummary:")
print(result.summary)

print("\nCompanies:")
for company in result.companies:
    print("-", company)

print("\nProducts:")
for product in result.products:
    print("-", product)

print("\nKey Points:")
for point in result.key_points:
    print("-", point)

print("\nSources:")
for source in result.sources:
    print("-", source)