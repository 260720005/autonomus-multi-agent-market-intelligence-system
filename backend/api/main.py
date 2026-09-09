from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # CORSMiddleware browser-based frontend ko backend ke saath communicate karne ki permission manage karta hai.
from pydantic import BaseModel, Field

from backend.graphs.research_graph import research_graph
from backend.models.report import ReportResult


app = FastAPI(
    title="Autonomus Multi Agent Market Intelligence System",
    description="API for the multi-agent market intelligence system",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware, # Origin b/w frontend and backend
    allow_origins=[
        "http://localhost:5173", # Both for frontend
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True, # Used for cookies
    allow_methods=["*"], # All HTTP methods allowed
    allow_headers=["*"], # Matlab frontend se different HTTP headers allow hain.
)


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=3)


class ResearchResponse(BaseModel):
    status: str
    query: str
    report: ReportResult


def create_initial_state(query: str):
    return {
        "user_query": query,
        "research_plan": None,
        "research_results": [],
        "market_results": [],
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


@app.get("/") # FASTAPI Decorator Jab user GET / request kare, neeche wala function execute karo.
def root(): #Endpoint function.
    return {
        "message": "Market Intelligence API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):

    initial_state = create_initial_state(request.query)

    try:
        result = research_graph.invoke(initial_state)

        return {
            "status": "success",
            "query": request.query,
            "report": result["report_result"]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Research pipeline failed: {str(e)}"
        )