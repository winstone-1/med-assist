#!/bin/bash
echo "Running seed..."
python seed.py
echo "Starting gunicorn..."
exec gunicorn app:app --workers 1 --bind 0.0.0.0:${PORT:-5000} --log-level info