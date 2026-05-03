# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import json

db = SQLAlchemy()

# ── Association table ─────────────────────────────────────────────────────────
symptom_condition = db.Table(
    'symptom_condition',
    db.Column('symptom_id',   db.Integer, db.ForeignKey('symptom.id'),   primary_key=True),
    db.Column('condition_id', db.Integer, db.ForeignKey('condition.id'), primary_key=True),
)


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id         = db.Column(db.Integer, primary_key=True)
    username   = db.Column(db.String(80),  unique=True, nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    history = db.relationship('SymptomHistory', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class SymptomHistory(db.Model):
    __tablename__ = 'symptom_history'

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answers_json = db.Column(db.Text)
    results_json = db.Column(db.Text)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def answers(self):
        return json.loads(self.answers_json) if self.answers_json else {}

    @property
    def results(self):
        return json.loads(self.results_json) if self.results_json else []

    def __repr__(self):
        return f'<SymptomHistory user={self.user_id}>'


class Symptom(db.Model):
    __tablename__ = 'symptom'

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(120), nullable=False, unique=True)
    slug        = db.Column(db.String(120), nullable=False, unique=True)
    body_area   = db.Column(db.String(60))
    description = db.Column(db.Text)

    conditions  = db.relationship(
        'Condition',
        secondary=symptom_condition,
        back_populates='symptoms'
    )

    def __repr__(self):
        return f'<Symptom {self.name}>'


class Condition(db.Model):
    __tablename__ = 'condition'

    id                 = db.Column(db.Integer, primary_key=True)
    name               = db.Column(db.String(120), nullable=False)
    severity           = db.Column(db.String(20),  default='low')
    description        = db.Column(db.Text)
    when_to_see_doctor = db.Column(db.Text)

    symptoms       = db.relationship(
        'Symptom',
        secondary=symptom_condition,
        back_populates='conditions'
    )
    firstaid_guide = db.relationship(
        'FirstAidGuide',
        backref='condition',
        uselist=False
    )

    def __repr__(self):
        return f'<Condition {self.name}>'


class Question(db.Model):
    __tablename__ = 'question'

    id            = db.Column(db.Integer, primary_key=True)
    text          = db.Column(db.String(300), nullable=False)
    question_type = db.Column(db.String(20),  default='checkbox')
    options_json  = db.Column(db.Text)
    order         = db.Column(db.Integer,     default=0)
    condition_id  = db.Column(db.Integer, db.ForeignKey('condition.id'), nullable=True)

    @property
    def options(self):
        return json.loads(self.options_json) if self.options_json else []

    def __repr__(self):
        return f'<Question {self.id}: {self.text[:40]}>'


class FirstAidGuide(db.Model):
    __tablename__ = 'firstaid_guide'

    id           = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(150), nullable=False)
    category     = db.Column(db.String(60))
    severity     = db.Column(db.String(20),  default='low')
    steps_json   = db.Column(db.Text,        nullable=False)
    warnings     = db.Column(db.Text)
    condition_id = db.Column(db.Integer, db.ForeignKey('condition.id'), nullable=True)

    @property
    def steps(self):
        return json.loads(self.steps_json) if self.steps_json else []

    def __repr__(self):
        return f'<FirstAidGuide {self.title}>'


class UserSession(db.Model):
    __tablename__ = 'user_session'

    id            = db.Column(db.Integer, primary_key=True)
    session_token = db.Column(db.String(64), unique=True, nullable=False)
    answers_json  = db.Column(db.Text)
    result_json   = db.Column(db.Text)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserSession {self.session_token[:8]}...>'