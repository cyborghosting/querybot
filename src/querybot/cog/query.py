import socket
import a2s
import discord
from discord import app_commands
from discord.ext import commands

from querybot.database import Database
from querybot.util import parse_host


class QueryCog(commands.Cog):
    def __init__(self, bot: commands.Bot, db: Database):
        self.bot = bot
        self.db = db

    async def _server_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        if (guild_id := interaction.guild_id) and (
            servers := await self.db.list_servers(guild_id)
        ):
            return [
                app_commands.Choice(name=server.name, value=server.name)
                for server in servers
                if current.lower() in server.name.lower()
            ]
        return []

    @app_commands.command(name="query", description="Query a game server.")
    @app_commands.autocomplete(query=_server_autocomplete)
    @app_commands.describe(query="The name of the game server.")
    async def query_server(self, interaction: discord.Interaction, query: str):
        if not (guild_id := interaction.guild_id):
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True
            )
            return

        await interaction.response.defer()

        if not (host := await self.db.get_server(guild_id, query)):
            host = parse_host(query)

        try:
            ip_address, port = socket.gethostbyname(host.hostname), host.port
        except socket.gaierror:
            await interaction.followup.send(
                f"Could not resolve hostname '{host.hostname}'."
            )
            return

        try:
            a2s_info = await a2s.ainfo((ip_address, port), 3.0, "UTF-8")
        except socket.timeout:
            await interaction.followup.send(
                f"Server '{host.hostname}:{host.port}' is offline."
            )
            return
        except socket.gaierror:
            await interaction.followup.send(
                f"Server '{host.hostname}:{host.port}' is unreachable."
            )
            return
        except:
            await interaction.followup.send(
                f"Error occurred while querying server '{host.hostname}:{host.port}'."
            )
            return

        embed = discord.Embed(title=a2s_info.server_name)
        embed.set_author(name="Server Information")
        embed.add_field(
            name="Host",
            value=f"[steam://connect/{host.hostname}:{host.port}](https://www.gaez.uk/steam/?hostname={ip_address}&port={port})",
            inline=False,
        )
        embed.add_field(name="Map", value=f"{a2s_info.map_name}", inline=True)
        embed.add_field(
            name="Players",
            value=f"{a2s_info.player_count}/{a2s_info.max_players}",
            inline=True,
        )
        embed.add_field(name="Game", value=f"{a2s_info.game}", inline=False)
        embed.set_footer(
            text=("VAC Secured" if a2s_info.vac_enabled else "Insecure")
            + (" + Password Protected" if a2s_info.password_protected else "")
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command(
        name="players", description="Get the player list from a game server."
    )
    @app_commands.autocomplete(query=_server_autocomplete)
    @app_commands.describe(query="The name of the game server.")
    async def query_players(self, interaction: discord.Interaction, query: str):
        if guild_id := interaction.guild_id:
            await interaction.response.defer()

            host = await self.db.get_server(guild_id, query)

            if not host:
                host = parse_host(query)

            try:
                a2s_players = await a2s.aplayers(
                    (host.hostname, host.port), 3.0, "UTF-8"
                )
            except socket.timeout:
                await interaction.followup.send(
                    f"Server '{host.hostname}:{host.port}' is offline."
                )
                return
            except socket.gaierror:
                await interaction.followup.send(
                    f"Server '{host.hostname}:{host.port}' is unreachable."
                )
                return
            except:
                await interaction.followup.send(
                    f"Error occurred while querying server '{host.hostname}:{host.port}'."
                )
                return

            if len(a2s_players) == 0:
                await interaction.followup.send("Server is empty!")
                return

            table = ""
            for player in a2s_players:
                hour, minute, name = (
                    int(player.duration) // 3600,
                    (int(player.duration) % 3600) // 60,
                    player.name,
                )
                table += f"{hour:02}:{minute:02} | {name}\n"
            await interaction.followup.send("```text\n" + str(table) + "\n```")
        else:
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True
            )
