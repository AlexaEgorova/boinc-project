from typing import List

from sqlmodel import SQLModel, Field

from models.objects import (
    ObjTable,
    ObjChair,
    ObjMisc
)
from models.rules import (
    RuleLevel
)


class StoreUpdateResult(SQLModel):
    """Store update result."""

    modified_count: int
    deleted_count: int


class Store(SQLModel):
    """Store."""

    rule_levels: List[RuleLevel] = Field(default_factory=list)
    tables: List[ObjTable] = Field(default_factory=list)
    chairs: List[ObjChair] = Field(default_factory=list)
    misc: List[ObjMisc] = Field(default_factory=list)
