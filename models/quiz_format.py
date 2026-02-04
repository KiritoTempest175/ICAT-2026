from pydantic import BaseModel
from typing import List

class Quiz(BaseModel):
    question: str
    options: List[str]
    answer: str