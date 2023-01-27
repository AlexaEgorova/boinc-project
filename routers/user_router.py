from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse, HTMLResponse

from config import GimmefyServerConfig
from models.users import User, UserFilled, UserTip
from servers.user_server import UserServer
from servers.server import AdminUser

config = GimmefyServerConfig()

server = UserServer(config=config)

router = APIRouter(
    tags=["users"],
)


@router.post(
    "/zpg/users",
    summary="Создать нового пользователя",
    response_model=User,
)
async def create_user(
    username: str,
    default_exp: int = config.default_exp,
    default_money: int = config.default_money,
    admin: AdminUser = Depends(server.admin_auth),
) -> User:
    """Создать нового пользователя."""
    return await server.create_user(
        username,
        default_exp,
        default_money
    )


@router.get(
    "/zpg/users/{username}",
    summary="Получить пользователя",
    response_model=User,
)
async def get_user(
    username: str,
    admin: AdminUser = Depends(server.admin_auth),
) -> User:
    """Получить пользователя."""
    return await server.get_user(username)


@router.get(
    "/zpg/users/{username}/filled",
    summary="Получить пользователя и все его предметы",
    response_model=UserFilled,
)
async def get_user_filled(
    username: str,
    admin: AdminUser = Depends(server.admin_auth),
) -> UserFilled:
    """Получить пользователя и все его предметы."""
    return await server.get_user_filled(username)


@router.post(
    "/zpg/users/{username}/promote",
    summary="Добавить пользователю опыта",
    response_model=User,
)
async def promote_user(
    username: str,
    exp_added: int,
    admin: AdminUser = Depends(server.admin_auth),
) -> User:
    """Добавить пользователю опыта."""
    return await server.promote_user(
        username,
        exp_added=exp_added
    )


@router.post(
    "/zpg/users/{username}/pay",
    summary="Добавить пользователю денег",
    response_model=User,
)
async def pay_user(
    username: str,
    money_added: int,
    admin: AdminUser = Depends(server.admin_auth),
) -> User:
    """Добавить пользователю денег."""
    return await server.pay_user(
        username,
        money_added=money_added
    )


@router.post(
    "/zpg/users/{username}/purchase/table/{table_id}",
    summary="Купить стол",
    response_model=User,
)
async def purchase_table(
    username: str,
    table_id: str,
    select_after_purchase: bool = True,
    admin: AdminUser = Depends(server.admin_auth),
) -> User:
    """Купить стол."""
    return await server.purchase_table(
        username,
        table_id,
        select_after_purchase
    )


@router.post(
    "/zpg/users/{username}/purchase/chair/{chair_id}",
    summary="Купить стул",
    response_model=User,
)
async def purchase_chair(
    username: str,
    chair_id: str,
    select_after_purchase: bool = True,
    admin: AdminUser = Depends(server.admin_auth),
) -> User:
    """Купить стул."""
    return await server.purchase_chair(
        username,
        chair_id,
        select_after_purchase
    )


@router.post(
    "/zpg/users/{username}/purchase/misc/{misc_id}",
    summary="Купить прочие предметы",
    response_model=User,
)
async def purchase_misc(
    username: str,
    misc_id: str,
    select_after_purchase: bool = True,
    admin: AdminUser = Depends(server.admin_auth),
) -> User:
    """Купить прочие предметы."""
    return await server.purchase_misc(
        username,
        misc_id,
        select_after_purchase
    )


@router.post(
    "/zpg/user/{username}/gender",
    summary="Сменить пол",
    response_class=RedirectResponse,
)
async def switch_gender(
    username: str,
    callback: Optional[str] = None
) -> RedirectResponse:
    """Сменить пол."""
    if callback is None:
        callback = server.config.base_url
    await server.switch_gender(
        username=username
    )
    return RedirectResponse(callback)


class ServerInfo(BaseModel):

    server: str = "gimmefy"
    info: str = "kekekeke"


@router.get(
    "/zpg/info",
    summary="Получить информацию",
    response_class=RedirectResponse,
)
async def get_info() -> RedirectResponse:
    """Получить информацию."""
    return RedirectResponse(
        url=server.config.base_url + "/assets/README.html"
    )


@router.get(
    "/zpg/user/{username}/theme",
    summary="Сменить пол",
    response_class=RedirectResponse,
)
async def get_switch_theme(
    username: str,
    callback: Optional[str] = None
) -> RedirectResponse:
    """Сменить пол."""
    if callback is None:
        callback = server.config.base_url
    await server.switch_theme(
        username=username
    )
    return RedirectResponse(callback)


@router.get(
    "/zpg/user/{username}/image",
    summary="Получить аватар",
    response_class=RedirectResponse,
)
async def get_avatar(
    username: str,
    expavg_score: float,
    cpus: int,
    registration_time: datetime,
    total_score: float = 0.0,
    has_android: bool = False
) -> RedirectResponse:
    """Получить аватар."""
    return await server.get_avatar(
        username=username,
        expavg_score=expavg_score,
        cpus=cpus,
        registration_time=registration_time,
        total_score=total_score,
        has_android=has_android
    )


@router.get(
    "/zpg/user/{username}/tip",
    summary="Получить совет",
    response_model=UserTip,
)
async def get_tip(
    username: str,
    expavg_score: float,
    cpus: int,
    registration_time: datetime,
    total_score: float = 0.0,
    has_android: bool = False
) -> UserTip:
    """Получить совет."""
    return await server.get_tip(
        username=username,
        expavg_score=expavg_score,
        cpus=cpus,
        registration_time=registration_time,
        total_score=total_score,
        has_android=has_android
    )


@router.get(
    "/zpg/user/{username}/level",
    summary="Получить уровень",
    response_model=User,
)
async def get_level(
    username: str,
    expavg_score: float,
    cpus: int,
    registration_time: datetime,
    total_score: float = 0.0,
    has_android: bool = False
) -> User:
    """Получить уровень."""
    return await server.get_level(
        username=username,
        expavg_score=expavg_score,
        cpus=cpus,
        registration_time=registration_time,
        total_score=total_score,
        has_android=has_android
    )
