"""Service server."""
import json

from models.store import Store, StoreUpdateResult
from models.objects import (
    ObjTable,
    ObjChair,
    ObjMisc,
)
from models.rules import RuleLevel
from helpers.objects import (
    upsert_obj,
    get_objs,
    delete_objs
)
from helpers.rules import (
    upsert_rule_level,
    get_rule_levels,
    delete_rule_levels,
    upsert_rule_item,
    get_rule_items,
    delete_rule_items
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
        rule_items = get_rule_items(self.db, {})
        return Store(
            rule_levels=rule_levels,
            rule_items=rule_items,
            tables=tables,
            chairs=chairs,
            misc=misc,
        )

    async def _update_store(
        self,
        store: Store
    ) -> StoreUpdateResult:
        modified_count = 0
        deleted_count = 0
        ids = []
        for table in store.tables:
            ids.append(table.id)
            modified_count += upsert_obj(self.db, table)
        deleted_count += delete_objs(
            db=self.db,
            filter={"id": {"$nin": ids}},
            type=ObjTable
        )

        ids = []
        for chair in store.chairs:
            ids.append(chair.id)
            modified_count += upsert_obj(self.db, chair)
        deleted_count += delete_objs(
            db=self.db,
            filter={"id": {"$nin": ids}},
            type=ObjChair
        )

        ids = []
        for misc in store.misc:
            ids.append(misc.id)
            modified_count += upsert_obj(self.db, misc)
        deleted_count += delete_objs(
            db=self.db,
            filter={"id": {"$nin": ids}},
            type=ObjMisc
        )

        levels = []
        for rule_level in store.rule_levels:
            levels.append(rule_level.level)
            modified_count += upsert_rule_level(self.db, rule_level)
        deleted_count += delete_rule_levels(
            db=self.db,
            filter={"level": {"$nin": levels}},
        )

        items = []
        for rule_item in store.rule_items:
            items.append(rule_item.item)
            modified_count += upsert_rule_item(self.db, rule_item)
        deleted_count += delete_rule_items(
            db=self.db,
            filter={"item": {"$nin": items}},
        )

        return StoreUpdateResult(
            modified_count=modified_count,
            deleted_count=deleted_count
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
