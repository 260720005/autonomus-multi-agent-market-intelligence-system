from pydantic import BaseModel, Field ##pydantic structures the LLm unstructured  

class ResearchPlan(BaseModel):

    market_tasks: list[str] = Field(
        description="Research tasks focused on market size, growth, funding, adoption, segmentation, and geography."
    )

    company_tasks: list[str] = Field(
        description="Research tasks focused on companies, products, competitors, positioning, partnerships, and capabilities."
    )

    trend_tasks: list[str] = Field(
        description="Research tasks focused on emerging trends, technologies, adoption patterns, signals, and future market direction."
    )