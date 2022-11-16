from typing import Optional, List

from mongo import Database, ObjectId

from models.users import User, UserFilled
from models.objects import (
    ObjTable,
    ObjChair,
    ObjMisc
)
from helpers.objects import get_obj_by_id, get_objs


def get_user_by_username(
    db: Database,
    username: str
) -> Optional[User]:
    """Get user by username."""
    data = db[User.__colname__].find_one(
        filter={"username": username}
    )
    if data is None:
        return None
    return User(**data)


def create_user(
    db: Database,
    user: User,
) -> ObjectId:
    """Create user."""
    return db[User.__colname__].insert_one(
        document=user.dict()
    ).inserted_id


def fill_in_user(
    db: Database,
    user: User,
) -> UserFilled:
    table_id = user.table
    chair_id = user.chair
    misc_ids = user.misc
    table = get_obj_by_id(db, table_id, ObjTable)
    if table is None:
        raise Exception(f"Table not found: {table_id}")
    chair = get_obj_by_id(db, chair_id, ObjChair)
    if chair is None:
        raise Exception(f"Chair not found: {chair_id}")
    misc: List[ObjMisc] = []
    for misc_id in misc_ids:
        misc_rec = get_obj_by_id(db, misc_id, ObjMisc)
        if misc_rec is None:
            raise Exception(f"Misc not found: {misc_id}")
        misc.append(misc_rec)
    owned_tables = get_objs(
        db,
        {"id": {"$in": user.owned_tables}},
        ObjTable
    )
    owned_chairs = get_objs(
        db,
        {"id": {"$in": user.owned_chairs}},
        ObjChair
    )
    owned_misc = get_objs(
        db,
        {"id": {"$in": user.owned_misc}},
        ObjMisc
    )

    return UserFilled(
        username=user.username,
        total_exp=user.total_exp,
        total_money=user.total_money,
        level=user.level,
        table=table,
        chair=chair,
        misc=misc,
        owned_tables=owned_tables,
        owned_chairs=owned_chairs,
        owned_misc=owned_misc
    )


def update_user(
    db: Database,
    user: User,
) -> int:
    """Create user."""
    return db[User.__colname__].update_one(
        filter={"username": user.username},
        update={"$set": user.dict()},
    ).modified_count
