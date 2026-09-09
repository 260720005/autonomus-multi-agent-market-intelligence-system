from pydantic import BaseModel, Field

class CriticResult(BaseModel):
    valid: bool = Field(
        description="Whether the research finding is reliable enough to use."
    )
    relevance_score: int = Field(
        description="How relevant the finding is to the research task, from task 0 to 10."
    )
    evidence_score: int = Field(
        description="How strongly the provided sources support the finding, from 0 to 10."
    )
    issues: list[str] = Field(
        description="Specific problems or weaknesses found in the research."
    )
    reason: str = Field(
        description="Explanation for why the finding was accepted or rejected."
    )
    needs_research: bool = Field(
        description="Whether the research task should be researched again."
    )