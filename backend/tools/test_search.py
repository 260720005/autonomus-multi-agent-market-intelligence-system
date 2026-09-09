from backend.tools.web_search import web_search
query="Latest Agentic AI market trends in 2026?"

results = web_search.invoke({
    "query": query
})

print("\n Search Results:\n")

for i, result in enumerate(results["results"], start = 1):
    print(f"\n --- Result {i} ---")
    print(f"Title", result["title"])
    print("URL:", result["url"])
    print("Score:", result["score"])
    print("Content:", result["content"][:500])