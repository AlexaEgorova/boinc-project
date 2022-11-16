"""Mongo client."""

# flake8: noqa
from mongo.db import MongoDBConfig, get_mongo_client
from pymongo.database import Database
from pymongo.collection import Collection
from bson import ObjectId
