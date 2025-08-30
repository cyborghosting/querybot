FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
RUN uv sync --locked

# Set environment variable for token (should be provided at runtime)
ENV TOKEN=""

# Run the bot
CMD ["uv", "run", "python", "src/main.py"]
