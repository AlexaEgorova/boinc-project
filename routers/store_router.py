from fastapi import APIRouter, Depends

from config import GimmefyServerConfig
from models.store import StoreUpdateResult, Store
from servers.store_server import ServiceServer
from servers.server import AdminUser

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
    admin: AdminUser = Depends(server.admin_auth)
) -> Store:
    """Получить данные объектов."""
    return await server.get_store()


@router.post(
    "/store",
    summary="Обновить бвзу объектов",
    response_model=StoreUpdateResult,
)
async def update_store(
    store: Store,
    admin: AdminUser = Depends(server.admin_auth)
) -> StoreUpdateResult:
    """Обновить бвзу объектов."""
    return await server.update_store(store)


@router.post(
    "/store/reload_internal",
    summary="Перезагрузить данные объектов из json",
    response_model=StoreUpdateResult,
)
async def reload_store(
    admin: AdminUser = Depends(server.admin_auth)
) -> StoreUpdateResult:
    """Перезагрузить данные объектов из json."""
    return await server.reload_store()
