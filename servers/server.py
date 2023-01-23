"""Base server."""
import json
from typing import Optional
from logging import Logger, getLogger

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
)

from sqlmodel import SQLModel

from models.store import Store

from config import GimmefyServerConfig
from mongo import get_mongo_client, Database

security = HTTPBasic(auto_error=False)


class AdminUser(SQLModel):

    username: str = "gimmefy_admin"
    password: str = "4RFV5tgb6YHN"



class Server:
    """Generic server."""

    def __init__(self, config: GimmefyServerConfig):
        """Initialize the server."""
        self.log: Logger = getLogger(self.__class__.__name__)

        self.db: Database = get_mongo_client(config.mongo)[config.mongo.db]
        self.config: GimmefyServerConfig = config

    def _user_auth_basic(
        self,
        credentials: HTTPBasicCredentials,
    ) -> AdminUser:
        user = AdminUser()
        if (
            credentials.username != user.username
            or credentials.password != user.password
        ):
            self.log.error(
                f"ERROR 401: "
                f"{credentials.password} "
                f" != 4RFV5tgb6YHN"
            )
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"}
            )
        return user

    def admin_auth(
        self,
        credentials: Optional[HTTPBasicCredentials] = Depends(security),
    ) -> AdminUser:
        if credentials is not None:
            return self._user_auth_basic(credentials)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication not provided",
        )

    def _reload_store(self):
        with self.config.store_path.open("r") as file:
            data = json.load(file)
            print(data)
        store = Store(**data)
        print(store)
        return await self._update_store(store)


