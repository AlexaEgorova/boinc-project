"""Base server."""
from typing import Optional
from logging import Logger, getLogger

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
)

from sqlmodel import SQLModel


import os
import argparse
import logging
import numpy as np
import torch
from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer)


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

        self.model, self.tokenizer = self._load_model()

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

    def _load_model(self):
        device = torch.device("cpu")
        model_class, tokenizer_class = (
            GPT2LMHeadModel,
            GPT2Tokenizer
        )
        self.tokenizer = tokenizer_class.from_pretrained(
            'sberbank-ai/rugpt3medium_based_on_gpt2'
        )
        self.model = model_class.from_pretrained(
            'sberbank-ai/rugpt3medium_based_on_gpt2'
        )
        self.model.to(device)
        return self.model, self.tokenizer