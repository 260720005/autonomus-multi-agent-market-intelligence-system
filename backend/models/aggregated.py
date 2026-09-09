#Aggregator = evidence ko arrange karta hai.
#Analyst = evidence ka meaning nikalta hai.
from pydantic import BaseModel
from backend.models.validated import ValidatedFinding

class AggregatedEvidence(BaseModel):
    market_evidence: list[ValidatedFinding]

    company_evidence: list[ValidatedFinding]

    trend_evidence: list[ValidatedFinding]