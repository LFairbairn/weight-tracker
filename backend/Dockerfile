# Start from an official Python image (slim = smaller size)
FROM python:3.10-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files first (allows Docker to cache this layer)
COPY pyproject.toml .python-version ./

# Install dependencies
RUN uv sync --no-dev --no-install-project

# Copy the rest of the application code
COPY . .

# Tell Docker which port the app will listen on
EXPOSE 8000

# Command to start the app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
