from contextlib import asynccontextmanager


class BaseRepository:
    def __init__(self, db, table):
        self.database = db
        self.table = table

    @classmethod
    @asynccontextmanager
    async def get_instance(cls, database, table):
        await database.connect()

        try:
            yield cls(database, table)
        finally:
            await database.disconnect()
