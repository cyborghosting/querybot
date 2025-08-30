import os
import sys

import discord
from discord.ext import commands

from querybot.cog.admin import AdminCog
from querybot.cog.query import QueryCog
from querybot.database import Database


class QueryBot(commands.Bot):
    def __init__(self, db: Database):
        self._db = db

        intents = discord.Intents.none()
        intents.message_content = True
        super().__init__(command_prefix="s!", intents=intents)

    async def setup_hook(self):
        await self.add_cog(QueryCog(self, self._db))
        await self.add_cog(AdminCog(self, self._db))

    async def on_ready(self):
        await self.tree.sync()


def main():
    token = os.getenv("TOKEN")
    if not token:
        print("No token found.")
        sys.exit(1)
    
    db_path = os.getenv("DB_PATH", "/querybot.sqlite3")
    bot = QueryBot(db=Database(db_path))

    bot.run(token)
    sys.exit(0)


if __name__ == "__main__":
    main()
