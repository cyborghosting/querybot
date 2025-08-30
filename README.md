# QueryBot

A Discord bot for querying Source engine game servers (CS:GO, TF2, etc.). Allows Discord server administrators to add game servers and users to query them for real-time information like player count, current map, and server status.

## Features

- **Server Management**: Administrators can add and remove game servers for their Discord server
- **Real-time Queries**: Users can query servers to get current player count, map, and server info
- **Autocomplete**: Smart autocomplete for server names when querying
- **Per-Guild Storage**: Each Discord server has its own list of configured game servers
- **Docker Support**: Easy deployment using Docker

## Prerequisites

- Python 3.13 or higher
- A Discord bot token
- uv package manager (optional, for development)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/querybot.git
   cd querybot
   ```

2. Build the Docker image:
   ```bash
   docker build -t querybot .
   ```

3. Run the bot:
   ```bash
   docker run -e TOKEN=your_discord_bot_token -e DB_PATH=/data/querybot.db -v /path/to/data:/data querybot
   ```

### Manual Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/querybot.git
   cd querybot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   # or using uv
   uv sync
   ```

3. Set environment variables:
   ```bash
   export TOKEN=your_discord_bot_token
   export DB_PATH=/path/to/database.db  # optional, defaults to /querybot.sqlite3
   ```

4. Run the bot:
   ```bash
   python src/main.py
   # or using uv
   uv run python src/main.py
   ```

## Configuration

The bot requires the following environment variables:

- `TOKEN`: Your Discord bot token (required)
- `DB_PATH`: Path to the SQLite database file (optional, defaults to `/querybot.sqlite3`)

## Usage

### Admin Commands

These commands require administrator permissions:

- `/addserver name:<name> hostname:<hostname> port:<port>` - Add a game server to the list
- `/removeserver name:<name>` - Remove a game server from the list
- `/listserver` - List all configured servers for this Discord server

### User Commands

- `/query query:<server_name>` - Query a configured server by name
- `/query query:<hostname:port>` - Query any server by hostname and port

## Supported Games

The bot supports querying any Source engine game server, including:
- Counter-Strike: Global Offensive (CS:GO)
- Team Fortress 2 (TF2)
- Garry's Mod
- And many more Source engine games

## Development

### Project Structure

```
src/
├── main.py              # Bot entry point
└── querybot/
    ├── database.py      # SQLite database operations
    ├── util.py          # Utility functions
    └── cog/
        ├── admin.py     # Admin commands
        └── query.py     # Query commands
```

### Dependencies

- `discord.py` - Discord API wrapper
- `aiosqlite` - Asynchronous SQLite database access
- `python-a2s` - Source engine server querying library

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.