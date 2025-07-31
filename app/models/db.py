from peewee import SqliteDatabase, Model, CharField
import os

DB_FILE = os.getenv("DB_FILE", "data/recommendations.db")
db = SqliteDatabase(DB_FILE)


class BaseModel(Model):
    class Meta:
        database = db


class Recommendation(BaseModel):
    id = CharField(primary_key=True)
    recommendation = CharField()
