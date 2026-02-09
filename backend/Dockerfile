# Stage 1: Builder
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /app

# Install uv for dependency management
RUN pip install uv

# Copy only the necessary files for dependency resolution
COPY backend/pyproject.toml backend/requirements.txt ./

# Install dependencies into a temporary directory
# This command installs packages into /usr/local/lib/python3.12/site-packages by default
# No need for uv venv if installing globally for the image
RUN uv pip install -r requirements.txt --system-site-packages

# Stage 2: Runner
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy the backend application code
COPY backend/ .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
