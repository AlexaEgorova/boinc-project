from typing import Optional, Type, overload, List

from mongo import Database, ObjectId

from models.objects import (
    ObjTable,
    ObjChair,
    ObjMisc,
    ObjBase
)


@overload
def get_obj_by_id(
    db: Database,
    id: str,
    type: Type[ObjTable]
) -> Optional[ObjTable]:
    """Get table by id."""
    ...


@overload
def get_obj_by_id(
    db: Database,
    id: str,
    type: Type[ObjChair]
) -> Optional[ObjChair]:
    """Get chair by id."""
    ...


@overload
def get_obj_by_id(
    db: Database,
    id: str,
    type: Type[ObjMisc]
) -> Optional[ObjMisc]:
    """Get misc by id."""
    ...


def get_obj_by_id(
    db: Database,
    id: str,
    type: Type[ObjBase]
) -> Optional[ObjBase]:
    """Get obj by id."""
    data = db[type.__colname__].find_one(
        filter={"id": id}
    )
    if data is None:
        return None
    return type(**data)


@overload
def get_objs(
    db: Database,
    filter: dict,
    type: Type[ObjTable]
) -> List[ObjTable]:
    """Get table by id."""
    ...


@overload
def get_objs(
    db: Database,
    filter: dict,
    type: Type[ObjChair]
) -> List[ObjChair]:
    """Get chair by id."""
    ...


@overload
def get_objs(
    db: Database,
    filter: dict,
    type: Type[ObjMisc]
) -> List[ObjMisc]:
    """Get misc by id."""
    ...


def get_objs(
    db: Database,
    filter: dict,
    type: Type[ObjBase]
) -> List[ObjBase]:
    """Get obj by id."""
    data = db[type.__colname__].find(
        filter=filter
    )
    resp: List[ObjBase] = []
    for rec in data:
        resp.append(type(**rec))
    return resp


@overload
def create_obj(
    db: Database,
    obj: ObjTable,
) -> ObjectId:
    """Create table."""
    ...


@overload
def create_obj(
    db: Database,
    obj: ObjChair,
) -> ObjectId:
    """Create chair."""
    ...


@overload
def create_obj(
    db: Database,
    obj: ObjMisc,
) -> ObjectId:
    """Create misc."""
    ...


def create_obj(
    db: Database,
    obj: ObjBase,
) -> ObjectId:
    """Create obj."""
    return db[obj.__colname__].insert_one(
        document=obj.dict()
    ).inserted_id


@overload
def update_obj(
    db: Database,
    obj: ObjTable,
) -> int:
    """Update table."""
    ...


@overload
def update_obj(
    db: Database,
    obj: ObjChair,
) -> int:
    """Update chair."""
    ...


@overload
def update_obj(
    db: Database,
    obj: ObjMisc,
) -> int:
    """Update misc."""
    ...


def update_obj(
    db: Database,
    obj: ObjBase,
) -> int:
    """Update obj."""
    return db[obj.__colname__].update_one(
        filter={"id": obj.id},
        update={"$set": obj.dict()},
    ).modified_count


@overload
def upsert_obj(
    db: Database,
    obj: ObjTable,
) -> int:
    """Upsert table."""
    ...


@overload
def upsert_obj(
    db: Database,
    obj: ObjChair,
) -> int:
    """Upsert chair."""
    ...


@overload
def upsert_obj(
    db: Database,
    obj: ObjMisc,
) -> int:
    """Upsert misc."""
    ...


def upsert_obj(
    db: Database,
    obj: ObjBase,
) -> int:
    """Create obj."""
    return db[obj.__colname__].update_one(
        filter={"id": obj.id},
        update={"$set": obj.dict()},
        upsert=True
    ).modified_count
