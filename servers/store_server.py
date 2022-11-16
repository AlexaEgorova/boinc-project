"""Service server."""
import json

from models.store import Store, StoreUpdateResult
from models.objects import (
    ObjTable,
    ObjChair,
    ObjMisc,
    ObjBase
)
from models.rules import RuleLevel
from helpers.objects import (
    upsert_obj,
    get_objs
)
from helpers.rules import (
    upsert_rule_level,
    get_rule_levels
)
from servers.server import Server


class ServiceServer(Server):
    """Service server."""

    async def get_store(
        self
    ) -> Store:
        tables = get_objs(self.db, {}, ObjTable)
        chairs = get_objs(self.db, {}, ObjChair)
        misc = get_objs(self.db, {}, ObjMisc)
        rule_levels = get_rule_levels(self.db, {})
        return Store(
            rule_levels=rule_levels,
            tables=tables,
            chairs=chairs,
            misc=misc,
        )

    async def _update_store(
        self,
        store: Store
    ) -> StoreUpdateResult:
        modified_count = 0
        for table in store.tables:
            modified_count += upsert_obj(self.db, table)
        for chair in store.chairs:
            modified_count += upsert_obj(self.db, chair)
        for misc in store.misc:
            modified_count += upsert_obj(self.db, misc)

        for rule_level in store.rule_levels:
            modified_count += upsert_rule_level(self.db, rule_level)

        return StoreUpdateResult(
            modified_count=modified_count
        )

    async def update_store(
        self,
        store: Store
    ) -> StoreUpdateResult:
        """Update database."""
        return await self._update_store(store)

    async def reload_store(
        self,
    ) -> StoreUpdateResult:
        """Reload database."""
        with self.config.store_path.open("r") as file:
            data = json.load(file)
            print(data)
        store = Store(**data)
        print(store)
        return await self._update_store(store)
