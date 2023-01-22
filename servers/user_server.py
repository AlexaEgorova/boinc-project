"""User server."""
from typing import Type, overload

from fastapi import status
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from models.users import User, UserFilled
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
    get_rule_level_by_exp
)
from servers.server import Server


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
            user.total_exp = total_exp
        rule = get_rule_level_by_exp(self.db, user.total_exp)
        if rule is None:
            return user
        if rule.level >= user.level:
            user.level = rule.level
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
        username: str
    ) -> User:
        """Get a user by username."""
        user = get_user_by_username(
            self.db,
            username
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
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
        user = await self.get_user(username)
        if user is None:
            user = await self.create_user(
                username=username,
                default_exp=0,
                default_money=0
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
        total_score: float
    ) -> RedirectResponse:
        """Get user avatar."""
        user = await self.get_user(username)
        if user is None:
            user = await self.create_user(
                username=username,
                default_exp=0,
                default_money=0
            )

        user = await self._promote_user(user, total_exp=total_score)

        img = f"{user.gender}_level_{user.level}.png"
        url = self.config.base_url + f"/assets/rendered/{img}"
        return RedirectResponse(url)
