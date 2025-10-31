# --- Stage 1: Builder Stage (for dependency installation) ---
# Use a Python base image with development headers for building C extensions (if any)
FROM python:3.11-slim AS builder

# Set the working directory
WORKDIR /app

# Install system dependencies needed for some Python packages (e.g., in a data science or DB environment)
# Customize this RUN command based on your application's needs (e.g., adding 'build-essential' or database clients)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage layer caching
COPY requirements.txt .

# Install production dependencies
# The --no-cache-dir flag is a good production practice.
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Production Runtime Stage (the final, minimal, and secure image) ---
# Use the smallest possible image that can run Python (e.g., alpine or a smaller slim image)
# We use a non-root user for security in this final stage.
FROM python:3.11-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy installed dependencies from the builder stage
# We use /usr/local/lib/python3.11/site-packages for standard pip installs
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# CRITICAL FIX: Copy the Python binary path (where 'uvicorn' and 'pip' executables live)
# This ensures the 'uvicorn' command is available in the final image's PATH.
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy your application code
COPY . /usr/src/app

# Define environment variables
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

# Expose the application port
EXPOSE 8000

# SECURITY: Create and switch to a non-root user (e.g., 'appuser')
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# The command to run your server (using Gunicorn as an example)
# Replace 'your_app.wsgi:application' with the correct entry point for your framework (e.g., Django, Flask)
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]
# CMD command execute from compose file 
CMD ["/bin/bash"]