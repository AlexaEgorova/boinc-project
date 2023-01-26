from typing import Optional, List

from mongo import Database, ObjectId

from models.rules import (
    RuleItem,
    RuleLevel
)


def get_rule_level_by_level(
    db: Database,
    level: int,
) -> Optional[RuleLevel]:
    """Get rule by level."""
    data = db[RuleLevel.__colname__].find_one(
        filter={"level": level}
    )
    if data is None:
        return None
    return RuleLevel(**data)


def get_rule_level_by_exp(
    db: Database,
    exp: float,
) -> Optional[RuleLevel]:
    """Get rule by level."""
    data = db[RuleLevel.__colname__].find_one(
        filter={"exp_gte": {"$lt": exp}},
        sort=[("exp_gte", -1)]
    )
    if data is None:
        return None
    return RuleLevel(**data)


def get_rule_item_by_level(
    db: Database,
    level: int,
) -> Optional[RuleItem]:
    """Get rule by level."""
    data = db[RuleItem.__colname__].find_one(
        filter={"level": level}
    )
    if data is None:
        return None
    return RuleItem(**data)


def get_rule_item_by_exp(
    db: Database,
    exp: float,
) -> Optional[RuleItem]:
    """Get rule by level."""
    data = db[RuleItem.__colname__].find_one(
        filter={"exp_gte": {"$lt": exp}},
        sort=[("exp_gte", -1)]
    )
    if data is None:
        return None
    return RuleItem(**data)


def get_rule_levels(
    db: Database,
    filter: dict
) -> List[RuleLevel]:
    """Get rule by level."""
    data = db[RuleLevel.__colname__].find(
        filter=filter
    )
    rules: List[RuleLevel] = []
    for rule in data:
        rules.append(RuleLevel(**rule))
    return rules


def create_rule_level(
    db: Database,
    rule: RuleLevel,
) -> ObjectId:
    """Create rule."""
    return db[rule.__colname__].insert_one(
        document=rule.dict()
    ).inserted_id


def update_rule_level(
    db: Database,
    rule: RuleLevel,
) -> int:
    """Update rule."""
    return db[rule.__colname__].update_one(
        filter={"id": rule.level},
        update={"$set": rule.dict()},
    ).modified_count


def upsert_rule_level(
    db: Database,
    rule: RuleLevel,
) -> int:
    """Create rule."""
    return db[rule.__colname__].update_one(
        filter={"id": rule.level},
        update={"$set": rule.dict()},
        upsert=True
    ).modified_count


def delete_rule_levels(
    db: Database,
    filter: dict
) -> int:
    """Delete rules."""
    return db[RuleLevel.__colname__].delete_many(
        filter=filter
    ).deleted_count
