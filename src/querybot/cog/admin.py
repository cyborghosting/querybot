import discord
from discord import app_commands
from discord.ext import commands

from querybot.database import Database


class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot, db: Database):
        self.bot = bot
        self.db = db

    async def _server_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        if guild_id := interaction.guild_id:
            servers = await self.db.list_servers(guild_id)
            if servers:
                return [
                    app_commands.Choice(name=server.name, value=server.name)
                    for server in servers
                    if current.lower() in server.name.lower()
                ]
            else:
                return []
        else:
            return []

    @app_commands.command(
        name="addserver", description="Add a game server to the list."
    )
    @app_commands.describe(
        name="The name of the game server.",
        hostname="The hostname or IP address of the game server.",
        port="The port number the game server is running on.",
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def add_server(
        self, interaction: discord.Interaction, name: str, hostname: str, port: int
    ):
        if guild_id := interaction.guild_id:
            await self.db.add_server(guild_id, name, hostname, port)
            await interaction.response.send_message(
                f"Server '{name}' added successfully."
            )

    @app_commands.command(
        name="removeserver", description="Remove a game server from the list."
    )
    @app_commands.describe(name="The name of the game server.")
    @app_commands.autocomplete(name=_server_autocomplete)
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_server(self, interaction: discord.Interaction, name: str):
        if guild_id := interaction.guild_id:
            await self.db.remove_server(guild_id, name)
            await interaction.response.send_message(
                f"Server '{name}' removed successfully."
            )

    @app_commands.command(name="listservers", description="List all game servers.")
    @app_commands.checks.has_permissions(administrator=True)
    async def list_servers(self, interaction: discord.Interaction):
        if guild_id := interaction.guild_id:
            servers = await self.db.list_servers(guild_id)
            if servers:
                embed = discord.Embed(
                    title="Game Servers", description="List of all game servers:"
                )
                for server in servers:
                    embed.add_field(
                        name=server.name,
                        value=f"Hostname: {server.host.hostname}\nPort: {server.host.port}",
                        inline=False,
                    )
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("No game servers found.")

    @add_server.error
    async def add_server_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You do not have permission to use this command."
            )
        else:
            await interaction.response.send_message(
                "An error occurred while adding the server."
            )

    @remove_server.error
    async def remove_server_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You do not have permission to use this command."
            )
        else:
            await interaction.response.send_message(
                "An error occurred while removing the server."
            )

    @list_servers.error
    async def list_servers_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "You do not have permission to use this command."
            )
        else:
            await interaction.response.send_message(
                "An error occurred while listing the servers."
            )
