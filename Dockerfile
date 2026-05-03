FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create instance directory
RUN mkdir -p instance

# Run seed (it will check if data exists and skip if already there)
RUN python seed.py

# Expose port
EXPOSE 5000

# Start the web server - THIS IS THE IMPORTANT PART
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]