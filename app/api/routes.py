from fastapi import APIRouter, HTTPException, Depends, Body
from app.models.schemas import PatientData, RecommendationResponse
from app.services.recommendation_engine import generate_recommendation
from app.models.db import Recommendation
from app.services.redis_client import cache_result, get_cached_result, publish_event
from app.auth.jwt import verify_token, create_token
import uuid

router = APIRouter()


@router.post("/login")
def login(username: str = Body(...), password: str = Body(...)):
    # hardcoded auth
    if username == "admin" and password == "admin123":
        token = create_token(user_id=username)
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid username or password")


@router.post("/evaluate", response_model=RecommendationResponse)
async def evaluate(data: PatientData, user=Depends(verify_token)):
    recommendation = generate_recommendation(data)
    rec_id = str(uuid.uuid4())

    Recommendation.create(id=rec_id, recommendation=recommendation)
    cache_result(rec_id, recommendation)
    publish_event(rec_id, data, recommendation)

    return RecommendationResponse(recommendation_id=rec_id, recommendation=recommendation)

@router.get("/recommendation/{rec_id}", response_model=RecommendationResponse)
async def get_recommendation(rec_id: str, user=Depends(verify_token)):
    recommendation = get_cached_result(rec_id)
    if recommendation:
        return RecommendationResponse(recommendation_id=rec_id, recommendation=recommendation)

    rec = Recommendation.get_or_none(Recommendation.id == rec_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found")

    return RecommendationResponse(recommendation_id=rec.id, recommendation=rec.recommendation)
