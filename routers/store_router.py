from fastapi import APIRouter

from config import GimmefyServerConfig
from models.store import StoreUpdateResult, Store
from servers.store_server import ServiceServer

config = GimmefyServerConfig()

server = ServiceServer(config=config)

router = APIRouter(
    tags=["store"],
)


@router.get(
    "/store",
    summary="Получить данные объектов",
    response_model=Store,
)
async def get_store(
) -> Store:
    """Получить данные объектов."""
    return await server.get_store()


@router.post(
    "/store",
    summary="Перезагрузить данные объектов",
    response_model=StoreUpdateResult,
)
async def update_store(
) -> StoreUpdateResult:
    """Перезагрузить данные объектов."""
    return await server.update_store()
