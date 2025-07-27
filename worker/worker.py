import redis
import json
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
CHANNEL_NAME = "recommendation_events"

def handle_event(event_data):
    print("Worker received event:")
    print(json.dumps(event_data, indent=2))
    # Simulate logging, email sending, etc.

def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    pubsub = r.pubsub()
    pubsub.subscribe(CHANNEL_NAME)

    print(f"Worker subscribed to channel: {CHANNEL_NAME}")
    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            handle_event(data)

if __name__ == "__main__":
    main()
