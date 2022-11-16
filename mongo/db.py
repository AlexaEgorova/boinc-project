"""Mongo db."""
import pytz
from pydantic import BaseModel
from pymongo import MongoClient


class MongoDBConfig(BaseModel):
    """Config for MongoDB."""

    host: str
    port: int
    username: str
    password: str
    db: str


def get_mongo_client(mongodb_config: MongoDBConfig) -> MongoClient:
    """Return mongodb connection."""
    url = "mongodb://{username}:{password}@{host}:{port}".format(
        username=mongodb_config.username,
        password=mongodb_config.password,
        host=mongodb_config.host,
        port=mongodb_config.port,
    )
    client: MongoClient = MongoClient(
        host=url,
        tz_aware=True,
        tzinfo=pytz.utc
    )
    return client
