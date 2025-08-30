import sqlite3

import aiosqlite

from querybot.util import Host, Server


# singleton class for sqlite database access
class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_name: str):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_name)

        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS "server" (
                    "guild_id" INTEGER NOT NULL,
                    "name" TEXT NOT NULL CHECK (LENGTH("name") <= 100),
                    "hostname" TEXT NOT NULL,
                    "port" INTEGER NOT NULL CHECK ("port" >= 0 AND "port" <= 65535),
                    PRIMARY KEY ("guild_id", "name")
                )
            """
            )

        conn.close()

    async def get_server(self, guild_id: int, name: str) -> Host | None:
        async with aiosqlite.connect(self.db_name) as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                """
                SELECT * FROM "server"
                WHERE "guild_id" = ? AND "name" = ?
            """,
                (guild_id, name),
            )
            if row := await cursor.fetchone():
                return Host(row[2], row[3])
            else:
                return None

    async def list_servers(self, guild_id: int) -> list[Server]:
        async with aiosqlite.connect(self.db_name) as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                """
                SELECT * FROM "server"
                WHERE "guild_id" = ?
            """,
                (guild_id,),
            )
            rows = await cursor.fetchall()
            return [Server(row[1], Host(row[2], row[3])) for row in rows]

    async def add_server(
        self, guild_id: int, name: str, hostname: str, port: int
    ) -> None:
        async with aiosqlite.connect(self.db_name) as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                """
                INSERT INTO "server" ("guild_id", "name", "hostname", "port")
                VALUES (?, ?, ?, ?)
            """,
                (guild_id, name, hostname, port),
            )
            await conn.commit()

    async def remove_server(self, guild_id: int, name: str) -> None:
        async with aiosqlite.connect(self.db_name) as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                """
                DELETE FROM "server"
                WHERE "guild_id" = ? AND "name" = ?
            """,
                (guild_id, name),
            )
            await conn.commit()

    async def autocomplete_server(self, guild_id: int, current: str) -> list[Server]:
        async with aiosqlite.connect(self.db_name) as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                """
                SELECT * FROM "server"
                WHERE "guild_id" = ? AND instr ("name", ?) = 1
                LIMIT 25
            """,
                (guild_id, current),
            )
            rows = await cursor.fetchall()
            return [Server(row[1], Host(row[2], row[3])) for row in rows]
