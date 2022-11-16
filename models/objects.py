import enum
from sqlmodel import SQLModel


class ObjsEnum(enum.Enum):

    TABLE = "TABLE"
    CHAIR = "CHAIR"
    MISC = "MISC"


class ObjBase(SQLModel):

    __colname__: str = 'non_set'

    id: str
    description: str
    asset: str
    cost: int
    min_level: int


class ObjTable(ObjBase):
    """Table object."""

    __colname__: str = 'lab_tables'


class ObjChair(ObjBase):
    """Chair object."""

    __colname__: str = 'lab_chairs'


class ObjMisc(ObjBase):
    """Misc object."""

    __colname__: str = 'lab_miscs'
