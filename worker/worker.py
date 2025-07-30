import redis
import json
import os
from datetime import datetime

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CHANNEL_NAME = "recommendation_events"
ANALYTICS_LOG = "worker/analytics.log"

def handle_event(event_data):
    print("Worker received event:")
    print(json.dumps(event_data, indent=2))

    # Simulate sending an email/SMS
    patient_id = event_data["patient_data"].get("id", "unknown")
    recommendation = event_data["recommendation"]
    print(f"Sending SMS/email to patient {patient_id}: '{recommendation}'")

    # Simulate report generation
    write_to_analytics_log(event_data)


def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL_NAME)

    print(f"Worker subscribed to channel: {CHANNEL_NAME}")
    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            handle_event(data)


def write_to_analytics_log(event):
    with open(ANALYTICS_LOG, "a") as f:
        f.write(f"{datetime.utcnow().isoformat()} | {json.dumps(event)}\n")


if __name__ == "__main__":
    main()
