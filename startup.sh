#!/bin/bash
python seed.py
gunicorn "app:create_app()" --bind 0.0.0.0:5000 --workers 1