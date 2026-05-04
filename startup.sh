#!/bin/bash
python seed.py
gunicorn app:app --bind 0.0.0.0:5000 --workers 1 --log-level debug 2>&1