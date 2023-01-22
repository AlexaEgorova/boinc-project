from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from config import GimmefyServerConfig

from servers.store_server import ServiceServer
from servers.server import AdminUser

config = GimmefyServerConfig()

server = ServiceServer(config=config)

router = APIRouter(
    tags=["image"],
)


level_map = {
    50: 2,
    200: 3,
    350: 4,
    500: 5,
    750: 6,
    1000: 7,
    1400: 8,
    1800: 9,
    2200: 10,
    2600: 11,
    3200: 12,
    4200: 13,
    6000: 14,
    7000: 15,
}


# @router.post(
#     "/img/{username}/gender",
#     summary="Сменить пол",
#     response_class=RedirectResponse,
# )
# async def change_gender(
# ) -> RedirectResponse:
#     """Получить данные объектов."""
#     return RedirectResponse()

router.mount("/assets", StaticFiles(directory="assets"), name="assets")

@router.get(
    "/img/{username}/score/{total_score}",
    summary="Получить изображение",
    response_class=RedirectResponse,
)
async def get_image(
    username: str,
    total_score: float
) -> RedirectResponse:
    """Получить данные объектов."""
    level = 1
    for score, lvl in level_map.items():
        if total_score >= score:
            level = lvl
    image_path = f"http://localhost:9192/assets/rendered/male_level_{level}.png"
    return RedirectResponse(image_path)
