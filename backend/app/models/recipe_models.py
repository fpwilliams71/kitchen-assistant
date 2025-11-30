from pydantic import BaseModel
from typing import List, Optional

class CookingRequest(BaseModel):
    recipe_name: str
    ingredients: List[str]

class QuestionRequest(BaseModel):
    question: str
    context: str = ""

class AIResponse(BaseModel):
    success: bool
    instructions: Optional[str] = None
    answer: Optional[str] = None
    error: Optional[str] = None