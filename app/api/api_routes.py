from fastapi import APIRouter, HTTPException
from app.models.schemas import PatientData, RecommendationResponse
from app.services.recommendation_engine import generate_recommendation
import uuid

router = APIRouter()

# Temporary in-memory store
recommendation_store = {}

@router.post("/evaluate", response_model=RecommendationResponse)
def evaluate(data: PatientData):
    recommendation = generate_recommendation(data)
    recommendation_id = str(uuid.uuid4())
    recommendation_store[recommendation_id] = recommendation
    return RecommendationResponse(recommendation_id=recommendation_id, recommendation=recommendation)

@router.get("/recommendation/{rec_id}", response_model=RecommendationResponse)
def get_recommendation(rec_id: str):
    recommendation = recommendation_store.get(rec_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return RecommendationResponse(recommendation_id=rec_id, recommendation=recommendation)

@router.get("/health")
def health_check():
    return {"status": "ok"}
