from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import PatientData, RecommendationResponse
from app.services.recommendation_engine import generate_recommendation
from app.auth.jwt import verify_token
from app.services.redis_client import cache_result, publish_event
import uuid

router = APIRouter()

# In-memory fallback store
recommendation_store = {}

@router.post("/evaluate", response_model=RecommendationResponse)
def evaluate(data: PatientData, user=Depends(verify_token)):
    recommendation = generate_recommendation(data)
    recommendation_id = str(uuid.uuid4())

    # Cache result in Redis
    cache_result(recommendation_id, recommendation)

    # Emit event for worker
    publish_event(recommendation_id, data, recommendation)

    # Optional in-memory store
    recommendation_store[recommendation_id] = recommendation

    return RecommendationResponse(
        recommendation_id=recommendation_id,
        recommendation=recommendation
    )

@router.get("/recommendation/{rec_id}", response_model=RecommendationResponse)
def get_recommendation(rec_id: str, user=Depends(verify_token)):
    from app.services.redis_client import get_cached_result

    recommendation = get_cached_result(rec_id)
    if not recommendation:
        recommendation = recommendation_store.get(rec_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return RecommendationResponse(recommendation_id=rec_id, recommendation=recommendation)
