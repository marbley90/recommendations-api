from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import PatientData, RecommendationResponse
from app.services.recommendation_engine import generate_recommendation
from app.models.db import Recommendation
from app.services.redis_client import cache_result, get_cached_result, publish_event
import uuid

router = APIRouter()

@router.post("/evaluate", response_model=RecommendationResponse)
async def evaluate(data: PatientData):
    recommendation = generate_recommendation(data)
    rec_id = str(uuid.uuid4())

    # Store in DB
    Recommendation.create(id=rec_id, recommendation=recommendation)

    # Optional: Cache and emit event
    cache_result(rec_id, recommendation)
    publish_event(rec_id, data, recommendation)

    return RecommendationResponse(recommendation_id=rec_id, recommendation=recommendation)

@router.get("/recommendation/{rec_id}", response_model=RecommendationResponse)
async def get_recommendation(rec_id: str):
    # Try Redis cache first
    recommendation = get_cached_result(rec_id)
    if recommendation:
        return RecommendationResponse(recommendation_id=rec_id, recommendation=recommendation)

    # Fallback to DB
    rec = Recommendation.get_or_none(Recommendation.id == rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    return RecommendationResponse(recommendation_id=rec.id, recommendation=rec.recommendation)
