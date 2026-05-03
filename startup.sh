#!/bin/bash
# Run seed if database is empty
python -c "
from app import create_app
from models import db, Symptom
app = create_app()
with app.app_context():
    if Symptom.query.count() == 0:
        import subprocess
        subprocess.run(['python', 'seed.py'])
"

# Start the app
gunicorn app:app --bind 0.0.0.0:5000