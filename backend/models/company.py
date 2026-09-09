from pydantic import BaseModel, Field

class CompanyFinding(BaseModel):
    task: str = Field(
        description="The company resarch task that was executed"
    )
    summary: str = Field(
        description="A concise summary of the competitive landscape or company findings."
    )

    companies: list[str] = Field(
        description="Important companies identified during the research."
    )

    products: list[str] = Field(
        description="Relevant AI products, platforms, or solutions identified."
    )

    key_points: list[str] = Field(
        description="Important factual information about the companies."
    )

    sources: list[str] = Field(
        description="URLs supporting the company-related findings."
    )