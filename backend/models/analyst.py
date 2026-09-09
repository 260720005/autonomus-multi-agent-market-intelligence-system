from pydantic import BaseModel

class AnalystResult(BaseModel):
    executive_summary: str

    market_insights: list[str]

    company_insights: list[str]

    trend_insights: list[str]

    growth_drivers: list[str]

    risks: list[str]

    opportunities: list[str]

    strategic_outlook: str