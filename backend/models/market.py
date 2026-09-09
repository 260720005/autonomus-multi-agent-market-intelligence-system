from pydantic import BaseModel, Field

class MarketFinding(BaseModel):
    task: str = Field(
        description="The market research task that was investigated"
    )

    summary: str = Field(
        description="A concise summary of the market related Findings."
    )

    key_points: list[str] = Field(
        description="Important factual market insights discovered."
    )

    metrics: list[str] = Field(
        description=(
            "Important quantitative market metrics such as market size, "
            "CAGR, growth rate, funding, adoption rate, or forecast."
        )
    )

    geography: list[str] = Field(
        description="Geographies or regions relevant to the findings."
    )

    sources: list[str] = Field(
        description="URLs of sources supporting the findings."
    )