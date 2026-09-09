from pydantic import BaseModel, Field

class ResearchFinding(BaseModel):
    task: str = Field(
        description="the resarch task that was investigated."
    )
    summary: str = Field(
        description="A concise summary of the findings."
    )

    key_points: list[str] = Field(
        description="Important factual points discovered during research."
    )

    sources: list[str] = Field(
        description="URLs of the sources used for the findings."
    )
