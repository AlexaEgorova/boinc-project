from sqlmodel import SQLModel


class RuleLevel(SQLModel):

    __colname__: str = 'rule_levels'

    level: int
    exp_gte: int


class RuleItem(SQLModel):

    __colname__: str = 'rule_items'

    item: str
    level: int
    exp_gte: int
