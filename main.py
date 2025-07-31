from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.models.db import db, Recommendation


app = FastAPI(
    title="Clinical Recommendation API",
    version="1.0.0",
    description="Mock clinical recommendation engine"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
def startup():
    db.connect()
    db.create_tables([Recommendation])


@app.on_event("shutdown")
def shutdown():
    if not db.is_closed():
        db.close()
