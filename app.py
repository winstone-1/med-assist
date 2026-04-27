# app.py
import os
from flask import Flask
from dotenv import load_dotenv
from models import db

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # ── Config ───────────────────────────────────────────────────────────────
    app.config['SECRET_KEY']                     = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI']        = os.getenv('DATABASE_URI', 'sqlite:///medassist.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ── Extensions ───────────────────────────────────────────────────────────
    db.init_app(app)

    # ── Create tables if they don't exist ────────────────────────────────────
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)