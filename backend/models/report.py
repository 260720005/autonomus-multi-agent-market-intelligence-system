## Difference between analyst result and report result is Analyst tell us What does the research tell
#  us and report result is how should we present those insights as a final report
from pydantic import BaseModel

class ReportResult(BaseModel):
    title: str
    executive_summary: str
    market_analysis: list[str]
    competitive_landscape: list[str]
    trend_analysis: list[str]
    growth_drivers: list[str]
    risks: list[str]
    opportunities: list[str]
    strategic_outlook: str