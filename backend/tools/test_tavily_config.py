from backend.config.config import TAVILY_API_KEY

if TAVILY_API_KEY:
    print("TAVILY_API_KEY loaded successfully!")
else:
    print("TAVILY_API_KEY not found.")