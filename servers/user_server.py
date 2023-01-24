"""User server."""
import math
from datetime import datetime
from typing import Type, overload

from fastapi import status
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException
from helpers.tip_gen import calc_score, tip_gen

from models.users import User, UserFilled, UserTip
from models.objects import (
    ObjTable,
    ObjChair,
    ObjMisc,
    ObjBase
)
from helpers.users import (
    get_user_by_username,
    fill_in_user,
    create_user,
    update_user
)
from helpers.objects import (
    get_obj_by_id
)
from helpers.rules import (
    get_rule_level_by_exp,
    get_rule_level_by_level
)
from servers.server import Server


LVL_MAP = {
    1: {"level_name": "абитуриент", "year": ""},
    2: {"level_name": "бакалавр", "year": "1 курс"},
    3: {"level_name": "бакалавр", "year": "2 курс"},
    4: {"level_name": "бакалавр", "year": "3 курс"},
    5: {"level_name": "бакалавр", "year": "4 курс"},
    6: {"level_name": "магистр", "year": "1 курс"},
    7: {"level_name": "магистр", "year": "2 курс"},
    8: {"level_name": "аспирант", "year": "1 курс"},
    9: {"level_name": "аспирант", "year": "2 курс"},
    10: {"level_name": "аспирант", "year": "3 курс"},
    11: {"level_name": "аспирант", "year": "4 курс"},
    12: {"level_name": "кандидат наук", "year": ""},
    13: {"level_name": "доктор наук", "year": ""},
    14: {"level_name": "доктор наук", "year": ""},
    15: {"level_name": "доктор наук", "year": ""},
}


class UserServer(Server):
    """User server."""

    async def _promote_user(
        self,
        user: User,
        exp_added: int = 0,
        total_exp: float = 0
    ) -> User:
        """Give exp to user."""
        if exp_added:
            user.total_exp += exp_added
        if total_exp:
            user.total_exp = max(user.total_exp, total_exp)
        rule = get_rule_level_by_exp(self.db, user.total_exp)
        if rule is None:
            return user
        if rule.level >= user.level:
            user.level = rule.level
        _map = LVL_MAP[user.level]
        user.level_name = _map["level_name"]
        user.year = _map["year"]
        update_user(self.db, user)
        return user

    async def _pay_user(
        self,
        user: User,
        money_added: int
    ) -> User:
        """Give money to user."""
        user.total_money += money_added
        update_user(self.db, user)
        return user

    async def create_user(
        self,
        username: str,
        default_exp: int,
        default_money: int,
    ):
        """Create a new user."""
        user = get_user_by_username(
            self.db,
            username
        )
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )
        user = User.create_new(
            username=username,
            default_exp=default_exp,
            default_money=default_money
        )
        create_user(self.db, user)
        user = await self._promote_user(user, 0)
        user = await self._pay_user(user, 0)
        return user

    async def get_user(
        self,
        username: str,
        do_create: bool = False,
    ) -> User:
        """Get a user by username."""
        user = get_user_by_username(
            self.db,
            username
        )
        if user is None:
            if not do_create:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
            user = await self.create_user(
                username=username,
                default_exp=0,
                default_money=0
            )
        return user

    async def get_user_filled(
        self,
        username: str
    ) -> UserFilled:
        """Get a user by username and fill in owned objects."""
        user = await self.get_user(username)
        try:
            user_filled = fill_in_user(self.db, user)
        except Exception as detail:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(detail)
            )
        return user_filled

    async def promote_user(
        self,
        username: str,
        exp_added: int
    ) -> User:
        """Add experience to user."""
        user: User = await self.get_user(username)
        return await self._promote_user(user, exp_added)

    async def pay_user(
        self,
        username: str,
        money_added: int
    ) -> User:
        """Add money to user."""
        user: User = await self.get_user(username)
        return await self._pay_user(user, money_added)

    @overload
    async def get_obj_by_id(
        self,
        obj_id: str,
        type: Type[ObjTable]
    ) -> ObjTable:
        ...

    @overload
    async def get_obj_by_id(
        self,
        obj_id: str,
        type: Type[ObjChair]
    ) -> ObjChair:
        ...

    @overload
    async def get_obj_by_id(
        self,
        obj_id: str,
        type: Type[ObjMisc]
    ) -> ObjMisc:
        ...

    async def get_obj_by_id(
        self,
        obj_id: str,
        type: Type[ObjBase]
    ):
        obj = get_obj_by_id(self.db, obj_id, type)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Object not found"
            )
        return obj

    async def purchase_table(
        self,
        username: str,
        table_id: str,
        select_after_purchase: bool
    ) -> User:
        user = await self.get_user(username)
        table: ObjTable = await self.get_obj_by_id(table_id, ObjTable)
        if table_id in user.owned_tables:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already ownes this table"
            )
        if user.total_money < table.cost:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough money"
            )
        user.total_money -= table.cost
        user.owned_tables.append(table_id)
        if select_after_purchase:
            user.table = table_id
        update_user(self.db, user)
        return user

    async def purchase_chair(
        self,
        username: str,
        chair_id: str,
        select_after_purchase: bool
    ) -> User:
        user = await self.get_user(username)
        chair: ObjChair = await self.get_obj_by_id(chair_id, ObjChair)
        if chair_id in user.owned_chairs:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already ownes this chair"
            )
        if user.total_money < chair.cost:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough money"
            )
        user.total_money -= chair.cost
        user.owned_chairs.append(chair_id)
        if select_after_purchase:
            user.chair = chair_id
        update_user(self.db, user)
        return user

    async def purchase_misc(
        self,
        username: str,
        misc_id: str,
        select_after_purchase: bool
    ) -> User:
        user = await self.get_user(username)
        misc: ObjMisc = await self.get_obj_by_id(misc_id, ObjMisc)
        if misc_id in user.owned_misc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already ownes this misc"
            )
        if user.total_money < misc.cost:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough money"
            )
        user.total_money -= misc.cost
        user.owned_misc.append(misc_id)
        if select_after_purchase:
            user.misc.append(misc_id)
        update_user(self.db, user)
        return user

    async def switch_gender(
        self,
        username: str
    ) -> Response:
        """Switch gender."""
        user = await self.get_user(
            username,
            do_create=True
        )
        if user.gender == 'male':
            user.gender = 'female'
        else:
            user.gender = 'male'
        update_user(self.db, user)
        return Response()

    async def get_avatar(
        self,
        username: str,
        total_score: float,
        expavg_score: float,
        cpus: int,
        registration_time: datetime,
    ) -> RedirectResponse:
        """Get user avatar."""
        user = await self.get_user(
            username,
            do_create=True
        )

        total_score = calc_score(
            total_score,
            expavg_score,
            cpus,
            registration_time,
        )
        user = await self._promote_user(user, total_exp=total_score)

        img = f"{user.gender}_level_{user.level}.png"
        url = self.config.base_url + f"/assets/rendered/{img}"
        return RedirectResponse(url)

    async def get_tip(
        self,
        username: str,
        total_score: float,
        expavg_score: float,
        cpus: int,
        registration_time: datetime,
    ) -> UserTip:
        """Get tip."""
        user = await self.get_user(
            username,
            do_create=True
        )

        total_score = calc_score(
            total_score,
            expavg_score,
            cpus,
            registration_time,
        )
        user = await self._promote_user(user, total_exp=total_score)

        return tip_gen(
            self.db,
            user,
            expavg_score,
            self.model,
            self.tokenizer,
        )

    async def get_level(
        self,
        username: str,
        total_score: float,
        expavg_score: float,
        cpus: int,
        registration_time: datetime,
    ) -> User:
        """Get user avatar."""
        user = await self.get_user(
            username,
            do_create=True
        )

        total_score = calc_score(
            expavg_score,
            cpus,
            registration_time,
        )
        user = await self._promote_user(user, total_exp=total_score)
        return user
