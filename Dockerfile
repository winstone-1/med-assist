FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the seeder to populate database
RUN python seed.py

# Expose the port
EXPOSE 5000

# Run the application with gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]