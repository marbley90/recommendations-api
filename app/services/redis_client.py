import redis
import os
import json
from app.models.schemas import PatientData

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CHANNEL_NAME = "recommendation_events"

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def cache_result(rec_id: str, recommendation: str):
    redis_client.setex(f"recommendation:{rec_id}", 3600, recommendation)

def get_cached_result(rec_id: str):
    return redis_client.get(f"recommendation:{rec_id}")

def publish_event(rec_id: str, patient_data: PatientData, recommendation: str):
    event = {
        "recommendation_id": rec_id,
        "patient_data": patient_data.dict(),
        "recommendation": recommendation
    }
    redis_client.publish(CHANNEL_NAME, json.dumps(event))
