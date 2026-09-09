from pydantic import BaseModel, Field

class TrendFinding(BaseModel):
    task: str = Field(
        description=" The trend research task that was investigated."
    )
    summary: str = Field(
        description="Important current or emerging trends identified."
    )
    
    trends: list[str] = Field(
        description="Important current or emerging trends identified."
    )

    signals: list[str] = Field(
        description="Evidence or signals indicating that a trend is emerging or accelerating."
    )

    impact: list[str] = Field(
        description="Potential business or market impact of the identified trends."
    )

    time_horizon: list[str] = Field(
        description="Time horizon associated with the trends, such as current, 1-2 years, or long-term."
    )

    sources: list[str] = Field(
        description="URLs supporting the trend findings."
    )