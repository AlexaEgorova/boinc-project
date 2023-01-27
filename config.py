"""Server config."""
from pathlib import Path

from pydantic import BaseSettings, Field

from mongo import MongoDBConfig


class EnvSettings(BaseSettings):
    """Base config for loading config from .env file."""

    class Config:
        """Overrides for BaseSettings model."""

        env_file = '.env'
        env_file_encoding = 'utf-8'


class MongoDBParams(MongoDBConfig, EnvSettings):
    """Config for mongo database."""

    host: str = Field(..., env="MONGO_HOST")
    port: int = Field(..., env="MONGO_PORT")
    username: str = Field(..., env="MONGO_USER")
    password: str = Field(..., env="MONGO_PASSWORD")
    db: str = Field(..., env="MONGO_DB")


class GimmefyServerConfig(EnvSettings):
    """Telemetry server configuration."""

    base_url: str = Field("http://localhost:9192", env="GIMMEFY_URL")

    default_exp: int = Field(0, env="GIMMEFY_DEFAULT_EXP")
    default_money: int = Field(200, env="GIMMEFY_DEFAULT_MONEY")

    mongo: MongoDBParams = MongoDBParams()  # type: ignore
    store_path: Path = Field(..., env="GIMMEFY_STORE_PATH")
