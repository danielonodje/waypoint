import uuid
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, String, Float
from sqlalchemy.sql import bindparam

from .base import BaseRepository
from waypoint.domain import Waypoint


async def get_waypoint_repository():
    metadata = MetaData()
    database = Database(get_connection_string())
    table = WaypointRepository.get_table_definition(metadata)

    engine = create_engine(get_connection_string(), echo=True)

    metadata.create_all(engine)

    async with WaypointRepository.get_instance(database, table) as repository:
        yield repository
        # await database.execute(query="DELETE FROM waypoints")


def get_connection_string():
    return "sqlite:///memory"


class WaypointRepository(BaseRepository):
    async def save(self, waypoint: Waypoint):
        query = self.table.insert()
        values = waypoint.to_dict()

        return await self.database.execute(query=query, values=values)

    async def list(self):
        query = self.table.select()
        waypoints = await self.database.fetch_all(query=query)

        return (
            [Waypoint.from_dict(waypoint) for waypoint in waypoints]
            if waypoints is not None
            else []
        )

    async def get(self, uuid: uuid.UUID):
        query = self.table.select().where(self.table.c.id == bindparam("id"))

        values = {"id": str(uuid)}

        result = await self.database.fetch_one(query=str(query), values=values)

        return Waypoint.from_dict(result) if result else None

    async def delete(self, uuid: uuid.UUID):
        query = self.table.delete().where(self.table.c.id == bindparam("id"))

        values = {"id": str(uuid)}

        await self.database.execute(query=str(query), values=values)

    @classmethod
    def get_table_definition(self, metadata):

        return Table(
            "waypoints",
            metadata,
            Column("id", String, primary_key=True),
            Column("latitude", Float),
            Column("longitude", Float),
        )
