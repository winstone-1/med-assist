# session_manager.py
from flask import session
import uuid


def init_session():
    """Initialise a fresh session for a new symptom check."""
    session.clear()
    session['answers'] = {}
    session['session_token'] = str(uuid.uuid4())
    session.modified = True


def save_answer(key: str, value):
    """Save a single answer to the session."""
    if 'answers' not in session:
        session['answers'] = {}
    session['answers'][key] = value
    session.modified = True


def get_answers() -> dict:
    """Retrieve all saved answers from the session."""
    return session.get('answers', {})


def clear_session():
    """Wipe the session after results are shown."""
    session.clear()


def get_session_token() -> str:
    """Get or create a unique session token."""
    if 'session_token' not in session:
        session['session_token'] = str(uuid.uuid4())
        session.modified = True
    return session['session_token']


def get_current_step() -> int:
    """Get the current step the user is on."""
    return session.get('current_step', 1)


def set_current_step(step: int):
    """Update the current step in session."""
    session['current_step'] = step
    session.modified = True


# Aliases for compatibility with app.py
def save_answers(key, value):
    """Alias for save_answer (compatibility)"""
    save_answer(key, value)