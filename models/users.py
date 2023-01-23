from datetime import datetime, timezone
from typing import List

from sqlmodel import SQLModel, Field

from models.objects import ObjTable, ObjChair, ObjMisc


class CharacterSet(SQLModel):

    glasses: str = Field("default")
    upperdress: str = Field("default")
    lowerdress: str = Field("default")


class User(SQLModel):
    """User."""

    __colname__: str = "users"  # type: ignore

    username: str
    gender: str = "male"

    last_online: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    level: int = 1
    total_exp: float
    total_money: int

    # character: CharacterSet = Field(default_factory=list)
    table: str = Field("default")
    chair: str = Field("default")
    misc: List[str] = Field(default_factory=list)

    owned_tables: List[str] = Field(default_factory=lambda: ["default"])
    owned_chairs: List[str] = Field(default_factory=lambda: ["default"])
    owned_misc: List[str] = Field(default_factory=list)

    @classmethod
    def create_new(
        cls,
        username: str,
        default_exp: int = 0,
        default_money: int = 200
    ):
        return cls(
            username=username,
            total_exp=default_exp,
            total_money=default_money,
            level=1,
            table="default",
            chair="default"
        )


class UserFilled(SQLModel):
    """User filled."""

    username: str
    gender: str = "male"

    level: int
    total_exp: int
    total_money: int

    table: ObjTable
    chair: ObjChair
    misc: List[ObjMisc] = Field(default_factory=list)

    owned_tables: List[ObjTable] = Field(default_factory=list)
    owned_chairs: List[ObjChair] = Field(default_factory=list)
    owned_misc: List[ObjMisc] = Field(default_factory=list)



class UserTip(SQLModel):
    """User tip."""

    text: str