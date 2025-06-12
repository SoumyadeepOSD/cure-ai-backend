# Use official Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy only requirements first (leverage Docker cache)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the codebase
COPY . .

# Expose the port (same as in main.py and startCommand)
EXPOSE 10000

# Set environment variables (DO NOT hardcode keys here, use Render's dashboard)
ENV PYTHONUNBUFFERED=1

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
