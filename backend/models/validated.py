# validated finding is made so that Jo findings Critic ke through validate ho chuki hain, unka clean combined version store karna.
# Jisse analyst ko bd me 3,4 cheez alg alg na btani pde
from pydantic import BaseModel
from typing import Any

from backend.models.critic import CriticResult

class ValidatedFinding(BaseModel):
    task:str
    type:str
    finding: Any
    critic: CriticResult