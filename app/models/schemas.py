from pydantic import BaseModel
from typing import Optional

class PatientData(BaseModel):
    age: int
    has_chronic_pain: bool = False
    bmi: float
    had_recent_surgery: bool = False

class RecommendationResponse(BaseModel):
    recommendation_id: str
    recommendation: str
