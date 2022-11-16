from fastapi import APIRouter, Depends
from pydantic import BaseModel

from config import GimmefyServerConfig
from models.users import User, UserFilled
from servers.user_server import UserServer

config = GimmefyServerConfig()

server = UserServer(config=config)

router = APIRouter(
    tags=["users"],
)


@router.post(
    "/users",
    summary="Создать нового пользователя",
    response_model=User,
)
async def create_user(
    username: str,
    default_exp: int = config.default_exp,
    default_money: int = config.default_money,
) -> User:
    """Создать нового пользователя."""
    return await server.create_user(
        username,
        default_exp,
        default_money
    )


@router.get(
    "/users/{username}",
    summary="Получить пользователя",
    response_model=User,
)
async def get_user(
    username: str
) -> User:
    """Получить пользователя."""
    return await server.get_user(username)


@router.get(
    "/users/{username}/filled",
    summary="Получить пользователя и все его предметы",
    response_model=UserFilled,
)
async def get_user_filled(
    username: str
) -> UserFilled:
    """Получить пользователя и все его предметы."""
    return await server.get_user_filled(username)


@router.post(
    "/users/{username}/promote",
    summary="Добавить пользователю опыта",
    response_model=User,
)
async def promote_user(
    username: str,
    exp_added: int
) -> User:
    """Добавить пользователю опыта."""
    return await server.promote_user(
        username,
        exp_added=exp_added
    )


@router.post(
    "/users/{username}/purchase/table/{table_id}",
    summary="Купить стол",
    response_model=User,
)
async def purchase_table(
    username: str,
    table_id: str,
    select_after_purchase: bool = True,
) -> User:
    """Купить стол."""
    return await server.purchase_table(
        username,
        table_id,
        select_after_purchase
    )


@router.post(
    "/users/{username}/purchase/chair/{chair_id}",
    summary="Купить стул",
    response_model=User,
)
async def purchase_chair(
    username: str,
    chair_id: str,
    select_after_purchase: bool = True,
) -> User:
    """Купить стул."""
    return await server.purchase_chair(
        username,
        chair_id,
        select_after_purchase
    )


@router.post(
    "/users/{username}/purchase/misc/{misc_id}",
    summary="Купить прочие предметы",
    response_model=User,
)
async def purchase_misc(
    username: str,
    misc_id: str,
    select_after_purchase: bool = True,
) -> User:
    """Купить прочие предметы."""
    return await server.purchase_misc(
        username,
        misc_id,
        select_after_purchase
    )
