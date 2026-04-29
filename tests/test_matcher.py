# tests/test_matcher.py
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from app import create_app
from models import db, Symptom, Condition
from symptom_matcher import match_symptoms, parse_answers, get_severity_label


@pytest.fixture
def app():
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def seeded_app(app):
    with app.app_context():
        s1 = Symptom(name='Fever',      slug='fever')
        s2 = Symptom(name='Cough',      slug='cough')
        s3 = Symptom(name='Chest Pain', slug='chest-pain')
        s4 = Symptom(name='Dizziness',  slug='dizziness')

        cold = Condition(
            name='Common Cold',
            severity='low',
            description='A cold.'
        )
        cold.symptoms = [s1, s2]

        heart = Condition(
            name='Heart Attack',
            severity='emergency',
            description='Emergency.'
        )
        heart.symptoms = [s3, s1, s4]

        db.session.add_all([cold, heart])
        db.session.commit()
    return app


# ── parse_answers tests ───────────────────────────────────────────────────────
def test_parse_answers_extracts_slugs(app):
    with app.app_context():
        parsed = parse_answers({'q_1': 'Fever,Cough'})
        assert 'fever' in parsed['symptom_slugs']
        assert 'cough' in parsed['symptom_slugs']


def test_parse_answers_duration(app):
    with app.app_context():
        parsed = parse_answers({'q_2': '1–3 days'})
        assert parsed['duration'] == '1–3 days'


def test_parse_answers_empty(app):
    with app.app_context():
        parsed = parse_answers({})
        assert parsed['symptom_slugs'] == set()
        assert parsed['duration'] is None


# ── match_symptoms tests ──────────────────────────────────────────────────────
def test_full_match(seeded_app):
    with seeded_app.app_context():
        results = match_symptoms({'q_1': 'Fever,Cough'})
        names   = [r['condition'].name for r in results]
        assert 'Common Cold' in names


def test_partial_match(seeded_app):
    with seeded_app.app_context():
        results = match_symptoms({'q_1': 'Fever'})
        assert len(results) >= 1


def test_no_match(seeded_app):
    with seeded_app.app_context():
        results = match_symptoms({'q_1': 'Rash'})
        assert results == []


def test_emergency_sorts_first(seeded_app):
    with seeded_app.app_context():
        results = match_symptoms({'q_1': 'Fever,Chest Pain,Dizziness'})
        assert results[0]['severity'] == 'emergency'


def test_score_between_0_and_1(seeded_app):
    with seeded_app.app_context():
        results = match_symptoms({'q_1': 'Fever,Cough'})
        for r in results:
            assert 0 <= r['base_score'] <= 1


# ── get_severity_label tests ──────────────────────────────────────────────────
def test_severity_label_emergency(app):
    with app.app_context():
        label = get_severity_label('emergency')
        assert label['label'] == 'Emergency'
        assert label['color'] == 'danger'


def test_severity_label_low(app):
    with app.app_context():
        label = get_severity_label('low')
        assert label['label'] == 'Low'
        assert label['color'] == 'success'


def test_severity_label_unknown(app):
    with app.app_context():
        label = get_severity_label('unknown')
        assert label['color'] == 'secondary'