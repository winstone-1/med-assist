# app.py
import os
import json
from flask import (
    Flask, render_template, request,
    session, redirect, url_for, flash
)
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from models import (
    db, User, SymptomHistory, Question, FirstAidGuide,
    MedicationReminder, HealthJournal, Appointment, BloodPressure, WellnessTip
)
from symptom_matcher import match_symptoms, get_severity_label
from api_client import get_drug_warnings
from session_manager import (
    save_answer, get_answers,
    clear_session, set_current_step
)
from datetime import datetime

load_dotenv()

bcrypt        = Bcrypt()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Config
    app.config['SECRET_KEY']                     = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI']        = os.getenv('DATABASE_URI', 'sqlite:///medassist.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view             = 'login'
    login_manager.login_message          = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    with app.app_context():
        db.create_all()

    # Auth Routes
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            email    = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            confirm  = request.form.get('confirm_password', '')

            if not username or not email or not password:
                flash('All fields are required.', 'danger')
                return render_template('register.html')
            if password != confirm:
                flash('Passwords do not match.', 'danger')
                return render_template('register.html')
            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'danger')
                return render_template('register.html')
            if User.query.filter_by(username=username).first():
                flash('Username already taken.', 'danger')
                return render_template('register.html')

            hashed = bcrypt.generate_password_hash(password).decode('utf-8')
            user   = User(username=username, email=email, password=hashed)
            db.session.add(user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            email    = request.form.get('email', '').strip()
            password = request.form.get('password', '')
            user     = User.query.filter_by(email=email).first()

            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                flash(f'Welcome back, {user.username}!', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash('Invalid email or password.', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        history = SymptomHistory.query.filter_by(
            user_id=current_user.id
        ).order_by(SymptomHistory.created_at.desc()).limit(10).all()
        return render_template('dashboard.html', history=history)

    @app.route('/profile')
    @login_required
    def profile():
        return render_template('profile.html')

    @app.route('/history/delete/<int:history_id>', methods=['POST'])
    @login_required
    def delete_history(history_id):
        record = SymptomHistory.query.get_or_404(history_id)
        if record.user_id != current_user.id:
            flash('Unauthorized.', 'danger')
            return redirect(url_for('dashboard'))
        db.session.delete(record)
        db.session.commit()
        flash('Record deleted.', 'success')
        return redirect(url_for('dashboard'))

    # Main Routes
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/symptom-checker', methods=['GET', 'POST'])
    def symptom_form():
        questions = Question.query.order_by(Question.order).all()
        total     = len(questions)
        step      = int(request.args.get('step', 1))

        if request.method == 'POST':
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

        for item in conditions:
            item['severity_info'] = get_severity_label(item['severity'])

        for item in conditions[:3]:
            item['drug_warnings'] = get_drug_warnings(item['condition'].name)

        has_emergency = any(i['severity'] == 'emergency' for i in conditions)

        if current_user.is_authenticated and conditions:
            results_data = [
                {
                    'condition': item['condition'].name,
                    'severity':  item['severity'],
                    'score':     item['final_score'],
                }
                for item in conditions
            ]
            history = SymptomHistory(
                user_id      = current_user.id,
                answers_json = json.dumps(answers),
                results_json = json.dumps(results_data),
            )
            db.session.add(history)
            db.session.commit()

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

    @app.route('/bmi-calculator', methods=['GET', 'POST'])
    def bmi_calculator():
        bmi_result = None
        if request.method == 'POST':
            try:
                weight = float(request.form.get('weight', 0))
                height = float(request.form.get('height', 0)) / 100
                if height > 0:
                    bmi = round(weight / (height ** 2), 1)
                    if bmi < 18.5:
                        category = 'Underweight'
                        color    = 'info'
                    elif bmi < 25:
                        category = 'Normal weight'
                        color    = 'success'
                    elif bmi < 30:
                        category = 'Overweight'
                        color    = 'warning'
                    else:
                        category = 'Obese'
                        color    = 'danger'
                    bmi_result = {
                        'bmi':      bmi,
                        'category': category,
                        'color':    color
                    }
            except (ValueError, ZeroDivisionError):
                flash('Please enter valid height and weight values.', 'danger')
        return render_template('bmi_calculator.html', bmi_result=bmi_result)

    @app.route('/emergency')
    def emergency():
        return render_template('emergency.html')

    @app.route('/disclaimer')
    def disclaimer():
        return render_template('disclaimer.html')

    # ============ HEALTH TOOLS ROUTES ============

    @app.route('/medications', methods=['GET', 'POST'])
    @login_required
    def medications():
        if request.method == 'POST':
            reminder = MedicationReminder(
                user_id=current_user.id,
                med_name=request.form.get('med_name'),
                dosage=request.form.get('dosage'),
                time_of_day=request.form.get('time_of_day'),
                frequency=request.form.get('frequency'),
                instructions=request.form.get('instructions')
            )
            db.session.add(reminder)
            db.session.commit()
            flash('Medication reminder added!', 'success')
            return redirect(url_for('medications'))
        
        reminders = MedicationReminder.query.filter_by(user_id=current_user.id).all()
        return render_template('medications.html', reminders=reminders)

    @app.route('/medication/delete/<int:med_id>', methods=['POST'])
    @login_required
    def delete_medication(med_id):
        med = MedicationReminder.query.get_or_404(med_id)
        if med.user_id == current_user.id:
            db.session.delete(med)
            db.session.commit()
            flash('Reminder deleted.', 'success')
        return redirect(url_for('medications'))

    @app.route('/journal', methods=['GET', 'POST'])
    @login_required
    def journal():
        if request.method == 'POST':
            entry = HealthJournal(
                user_id=current_user.id,
                entry_date=datetime.strptime(request.form.get('entry_date'), '%Y-%m-%d'),
                mood=int(request.form.get('mood')),
                symptoms=request.form.get('symptoms'),
                notes=request.form.get('notes')
            )
            db.session.add(entry)
            db.session.commit()
            flash('Journal entry saved!', 'success')
            return redirect(url_for('journal'))
        
        entries = HealthJournal.query.filter_by(user_id=current_user.id).order_by(HealthJournal.entry_date.desc()).all()
        today = datetime.now().strftime('%Y-%m-%d')
        return render_template('journal.html', entries=entries, today=today)

    @app.route('/journal/delete/<int:entry_id>', methods=['POST'])
    @login_required
    def delete_journal(entry_id):
        entry = HealthJournal.query.get_or_404(entry_id)
        if entry.user_id == current_user.id:
            db.session.delete(entry)
            db.session.commit()
            flash('Journal entry deleted.', 'success')
        return redirect(url_for('journal'))

    @app.route('/appointments', methods=['GET', 'POST'])
    @login_required
    def appointments():
        if request.method == 'POST':
            apt = Appointment(
                user_id=current_user.id,
                doctor_name=request.form.get('doctor_name'),
                specialty=request.form.get('specialty'),
                appointment_date=datetime.strptime(request.form.get('appointment_date'), '%Y-%m-%d'),
                appointment_time=request.form.get('appointment_time'),
                location=request.form.get('location'),
                notes=request.form.get('notes')
            )
            db.session.add(apt)
            db.session.commit()
            flash('Appointment scheduled!', 'success')
            return redirect(url_for('appointments'))
        
        appointments_list = Appointment.query.filter_by(user_id=current_user.id).order_by(Appointment.appointment_date).all()
        return render_template('appointments.html', appointments=appointments_list)

    @app.route('/appointment/delete/<int:appointment_id>', methods=['POST'])
    @login_required
    def delete_appointment(appointment_id):
        apt = Appointment.query.get_or_404(appointment_id)
        if apt.user_id == current_user.id:
            db.session.delete(apt)
            db.session.commit()
            flash('Appointment cancelled.', 'success')
        return redirect(url_for('appointments'))

    @app.route('/bp-tracker', methods=['GET', 'POST'])
    @login_required
    def bp_tracker():
        if request.method == 'POST':
            pulse = request.form.get('pulse')
            reading = BloodPressure(
                user_id=current_user.id,
                systolic=int(request.form.get('systolic')),
                diastolic=int(request.form.get('diastolic')),
                pulse=int(pulse) if pulse else None,
                reading_date=datetime.strptime(request.form.get('reading_date'), '%Y-%m-%d'),
                notes=request.form.get('notes')
            )
            db.session.add(reading)
            db.session.commit()
            flash('Blood pressure reading saved!', 'success')
            return redirect(url_for('bp_tracker'))
        
        readings = BloodPressure.query.filter_by(user_id=current_user.id).order_by(BloodPressure.reading_date.desc()).all()
        today = datetime.now().strftime('%Y-%m-%d')
        return render_template('bp_tracker.html', readings=readings, today=today)

    @app.route('/bp-reading/delete/<int:reading_id>', methods=['POST'])
    @login_required
    def delete_bp_reading(reading_id):
        reading = BloodPressure.query.get_or_404(reading_id)
        if reading.user_id == current_user.id:
            db.session.delete(reading)
            db.session.commit()
            flash('Reading deleted.', 'success')
        return redirect(url_for('bp_tracker'))

    @app.route('/wellness')
    def wellness():
        category = request.args.get('category')
        if category:
            tips = WellnessTip.query.filter_by(category=category).all()
        else:
            tips = WellnessTip.query.all()
        return render_template('wellness.html', tips=tips, current_category=category)

    # ============ GOOGLE LOGIN ROUTE ============
    @app.route('/google-login', methods=['POST'])
    def google_login():
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        google_id = data.get('google_id')
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            username = name.replace(' ', '').lower() + str(int(datetime.now().timestamp()))[-4:]
            user = User(
                username=username,
                email=email,
                password=bcrypt.generate_password_hash(google_id).decode('utf-8')
            )
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        return json.dumps({'success': True})

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app


# Create app instance for Render
app = create_app()

# Run only when executed directly (not on Render)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)