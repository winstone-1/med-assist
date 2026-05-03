FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p instance

# DO NOT run seed here
# RUN python seed.py

EXPOSE 5000

# Start gunicorn only - seed will run in app if needed
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--timeout", "120"]