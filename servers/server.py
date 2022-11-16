"""Base server."""
from logging import Logger, getLogger

from config import GimmefyServerConfig
from mongo import get_mongo_client, Database


class Server:
    """Generic server."""

    def __init__(self, config: GimmefyServerConfig):
        """Initialize the server."""
        self.log: Logger = getLogger(self.__class__.__name__)

        self.db: Database = get_mongo_client(config.mongo)[config.mongo.db]
        self.config: GimmefyServerConfig = config
