# app.py
import os
from flask import (
    Flask, render_template, request,
    session, redirect, url_for, send_file
)
from dotenv import load_dotenv
from models import db, Question, FirstAidGuide
from symptom_matcher import match_symptoms, get_severity_label
from api_client import get_drug_warnings
from session_manager import (
    init_session, save_answer, get_answers,
    clear_session, get_session_token, set_current_step
)

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # ── Config ───────────────────────────────────────────────────────────────
    app.config['SECRET_KEY']                     = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI']        = os.getenv('DATABASE_URI', 'sqlite:///medassist.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ── Extensions ───────────────────────────────────────────────────────────
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ── Routes ───────────────────────────────────────────────────────────────

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/symptom-checker', methods=['GET', 'POST'])
    def symptom_form():
        questions = Question.query.order_by(Question.order).all()
        total     = len(questions)
        step      = int(request.args.get('step', 1))

        if request.method == 'POST':
            # ── Save answers to session via session manager ──────────────────
            for key, value in request.form.items():
                save_answer(key, value)
            set_current_step(step + 1)

            if step < total:
                return redirect(url_for('symptom_form', step=step + 1))
            return redirect(url_for('results'))

        question = questions[step - 1] if questions else None
        return render_template(
            'symptom_form.html',
            question=question,
            step=step,
            total=total
        )

    @app.route('/results')
    def results():
        answers    = get_answers()
        conditions = match_symptoms(answers)

        # ── Attach severity labels ───────────────────────────────────────────
        for item in conditions:
            item['severity_info'] = get_severity_label(item['severity'])

        # ── Fetch OpenFDA drug warnings for top 3 matches ────────────────────
        for item in conditions[:3]:
            item['drug_warnings'] = get_drug_warnings(item['condition'].name)

        # ── Check if any emergency condition matched ─────────────────────────
        has_emergency = any(i['severity'] == 'emergency' for i in conditions)

        return render_template(
            'results.html',
            conditions=conditions,
            has_emergency=has_emergency
        )

    @app.route('/clear')
    def clear():
        clear_session()
        return redirect(url_for('symptom_form'))

    @app.route('/first-aid')
    def firstaid_list():
        guides = FirstAidGuide.query.order_by(FirstAidGuide.severity).all()
        return render_template('firstaid_list.html', guides=guides)

    @app.route('/first-aid/<int:guide_id>')
    def firstaid_detail(guide_id):
        guide = FirstAidGuide.query.get_or_404(guide_id)
        return render_template('firstaid_detail.html', guide=guide)

    @app.route('/emergency')
    def emergency():
        return render_template('emergency.html')

    @app.route('/disclaimer')
    def disclaimer():
        return render_template('disclaimer.html')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)