# seed.py
import json
import os
from app import create_app
from models import db, Symptom, Condition, Question, FirstAidGuide

app = create_app()

# ── Symptoms ─────────────────────────────────────────────────────────────────
SYMPTOMS = [
    {'name': 'Fever',               'slug': 'fever',               'body_area': 'systemic',    'description': 'Elevated body temperature above 38°C'},
    {'name': 'Headache',            'slug': 'headache',            'body_area': 'head',        'description': 'Pain or pressure in the head'},
    {'name': 'Cough',               'slug': 'cough',               'body_area': 'respiratory', 'description': 'Sudden expulsion of air from the lungs'},
    {'name': 'Sore Throat',         'slug': 'sore-throat',         'body_area': 'throat',      'description': 'Pain or irritation in the throat'},
    {'name': 'Fatigue',             'slug': 'fatigue',             'body_area': 'systemic',    'description': 'Extreme tiredness and lack of energy'},
    {'name': 'Nausea',              'slug': 'nausea',              'body_area': 'abdomen',     'description': 'Feeling of sickness with an inclination to vomit'},
    {'name': 'Vomiting',            'slug': 'vomiting',            'body_area': 'abdomen',     'description': 'Forceful expulsion of stomach contents'},
    {'name': 'Diarrhoea',           'slug': 'diarrhoea',           'body_area': 'abdomen',     'description': 'Loose or watery stools more than 3 times per day'},
    {'name': 'Abdominal Pain',      'slug': 'abdominal-pain',      'body_area': 'abdomen',     'description': 'Pain or discomfort in the stomach area'},
    {'name': 'Chest Pain',          'slug': 'chest-pain',          'body_area': 'chest',       'description': 'Pain, pressure, or tightness in the chest'},
    {'name': 'Shortness of Breath', 'slug': 'shortness-of-breath', 'body_area': 'chest',       'description': 'Difficulty breathing or feeling breathless'},
    {'name': 'Dizziness',           'slug': 'dizziness',           'body_area': 'head',        'description': 'Feeling faint, unsteady, or lightheaded'},
    {'name': 'Rash',                'slug': 'rash',                'body_area': 'skin',        'description': 'Skin irritation, redness, or bumps'},
    {'name': 'Runny Nose',          'slug': 'runny-nose',          'body_area': 'head',        'description': 'Excess discharge from the nasal passages'},
    {'name': 'Body Aches',          'slug': 'body-aches',          'body_area': 'systemic',    'description': 'General muscle pain throughout the body'},
    {'name': 'Loss of Appetite',    'slug': 'loss-of-appetite',    'body_area': 'systemic',    'description': 'Reduced desire to eat'},
    {'name': 'Sweating',            'slug': 'sweating',            'body_area': 'systemic',    'description': 'Excessive perspiration'},
    {'name': 'Chills',              'slug': 'chills',              'body_area': 'systemic',    'description': 'Feeling of coldness with shivering'},
    {'name': 'Swollen Lymph Nodes', 'slug': 'swollen-lymph-nodes', 'body_area': 'throat',      'description': 'Enlarged glands in the neck, armpits, or groin'},
    {'name': 'Eye Redness',         'slug': 'eye-redness',         'body_area': 'head',        'description': 'Red or irritated eyes'},
]

# ── Conditions ────────────────────────────────────────────────────────────────
CONDITIONS = [
    {
        'name':               'Common Cold',
        'severity':           'low',
        'description':        'A viral infection of the upper respiratory tract. Usually harmless and resolves within 7–10 days.',
        'when_to_see_doctor': 'If symptoms last more than 10 days, worsen after improving, or include high fever above 39°C.',
        'symptom_slugs':      ['runny-nose', 'sore-throat', 'cough', 'headache', 'fatigue', 'fever'],
    },
    {
        'name':               'Influenza (Flu)',
        'severity':           'moderate',
        'description':        'A contagious respiratory illness caused by influenza viruses. More severe than a cold with sudden onset.',
        'when_to_see_doctor': 'If you have difficulty breathing, persistent chest pain, severe vomiting, or are in a high-risk group.',
        'symptom_slugs':      ['fever', 'chills', 'body-aches', 'headache', 'fatigue', 'cough', 'sore-throat', 'loss-of-appetite'],
    },
    {
        'name':               'Gastroenteritis (Stomach Flu)',
        'severity':           'moderate',
        'description':        'Inflammation of the stomach and intestines, usually caused by a viral or bacterial infection.',
        'when_to_see_doctor': 'If diarrhoea contains blood, vomiting persists more than 2 days, or signs of dehydration appear.',
        'symptom_slugs':      ['nausea', 'vomiting', 'diarrhoea', 'abdominal-pain', 'fever', 'loss-of-appetite'],
    },
    {
        'name':               'Strep Throat',
        'severity':           'moderate',
        'description':        'A bacterial throat infection caused by Streptococcus. Requires antibiotic treatment.',
        'when_to_see_doctor': 'See a doctor promptly — strep requires antibiotics and can lead to complications if untreated.',
        'symptom_slugs':      ['sore-throat', 'fever', 'swollen-lymph-nodes', 'headache', 'loss-of-appetite'],
    },
    {
        'name':               'Malaria',
        'severity':           'urgent',
        'description':        'A serious mosquito-borne disease common in tropical regions including Kenya. Requires immediate treatment.',
        'when_to_see_doctor': 'Seek medical attention immediately if malaria is suspected — it can become life-threatening rapidly.',
        'symptom_slugs':      ['fever', 'chills', 'sweating', 'headache', 'nausea', 'vomiting', 'body-aches', 'fatigue'],
    },
    {
        'name':               'Typhoid Fever',
        'severity':           'urgent',
        'description':        'A bacterial infection caused by Salmonella typhi. Common in areas with poor sanitation.',
        'when_to_see_doctor': 'Seek medical care immediately — typhoid needs antibiotics and can be severe if delayed.',
        'symptom_slugs':      ['fever', 'headache', 'abdominal-pain', 'loss-of-appetite', 'fatigue', 'rash'],
    },
    {
        'name':               'Heart Attack',
        'severity':           'emergency',
        'description':        'A blockage of blood flow to the heart muscle. Every minute without treatment causes damage.',
        'when_to_see_doctor': 'Call emergency services (999/112) IMMEDIATELY. Do not drive yourself to hospital.',
        'symptom_slugs':      ['chest-pain', 'shortness-of-breath', 'nausea', 'sweating', 'dizziness', 'fatigue'],
    },
    {
        'name':               'Allergic Reaction',
        'severity':           'urgent',
        'description':        'An immune system response to a foreign substance. Ranges from mild to life-threatening anaphylaxis.',
        'when_to_see_doctor': 'Seek emergency care immediately if throat swelling, difficulty breathing, or severe rash develops.',
        'symptom_slugs':      ['rash', 'shortness-of-breath', 'nausea', 'dizziness', 'eye-redness'],
    },
]

# ── Questions ─────────────────────────────────────────────────────────────────
QUESTIONS = [
    {
        'text':          'Which of the following symptoms are you currently experiencing? (Select all that apply)',
        'question_type': 'checkbox',
        'order':         1,
        'options':       [
            'Fever', 'Headache', 'Cough', 'Sore Throat', 'Fatigue',
            'Nausea', 'Vomiting', 'Diarrhoea', 'Abdominal Pain',
            'Chest Pain', 'Shortness of Breath', 'Dizziness',
            'Rash', 'Runny Nose', 'Body Aches', 'Loss of Appetite',
            'Sweating', 'Chills', 'Swollen Lymph Nodes', 'Eye Redness',
        ],
    },
    {
        'text':          'How long have you been experiencing these symptoms?',
        'question_type': 'radio',
        'order':         2,
        'options':       ['Less than 24 hours', '1–3 days', '4–7 days', 'More than a week'],
    },
    {
        'text':          'How would you describe the overall severity of your symptoms?',
        'question_type': 'radio',
        'order':         3,
        'options':       [
            'Mild — I can manage daily activities',
            'Moderate — I am struggling with some activities',
            'Severe — I cannot do daily activities',
            'Critical — I need immediate help',
        ],
    },
    {
        'text':          'Do you have any of the following high-risk factors?',
        'question_type': 'checkbox',
        'order':         4,
        'options':       [
            'I am over 60 years old',
            'I have a chronic illness (diabetes, heart disease, etc.)',
            'I am pregnant',
            'I have a weakened immune system',
            'None of the above',
        ],
    },
]

# ── First Aid Guides ──────────────────────────────────────────────────────────
FIRST_AID_GUIDES = [
    {
        'title':    'First Aid for Choking (Adult)',
        'category': 'choking',
        'severity': 'emergency',
        'steps': [
            'Ask loudly: "Are you choking?" — if they cannot speak, cough, or breathe, act immediately.',
            'Call or ask someone to call emergency services (999 / 112).',
            'Lean the person forward and give 5 firm back blows between the shoulder blades with the heel of your hand.',
            'Check their mouth — if the object is visible, carefully remove it. Do not do blind finger sweeps.',
            'Give 5 abdominal thrusts (Heimlich): stand behind, make a fist above the navel, pull sharply inward and upward.',
            'Alternate 5 back blows and 5 abdominal thrusts until the obstruction is cleared or help arrives.',
            'If the person becomes unconscious, lower them carefully and begin CPR immediately.',
        ],
        'warnings': 'Do NOT perform abdominal thrusts on infants under 1 year old or on pregnant persons — use chest thrusts instead.',
    },
    {
        'title':    'First Aid for Burns (Minor)',
        'category': 'burns',
        'severity': 'moderate',
        'steps': [
            'Remove the person from the source of the burn immediately.',
            'Cool the burn under cool (not cold, not icy) running water for at least 20 minutes.',
            'Remove jewellery, watches, or tight clothing near the burn before swelling begins.',
            'Cover loosely with a sterile, non-fluffy dressing or clean cling film.',
            'Do NOT apply butter, toothpaste, ice, or any home remedy — these make burns worse.',
            'Take paracetamol or ibuprofen for pain relief if not contraindicated.',
            'Seek medical attention if the burn is larger than the person\'s palm or covers the face, hands, or feet.',
        ],
        'warnings': 'Seek emergency care immediately for burns covering more than 10% of the body, all 3rd-degree burns, and chemical or electrical burns.',
    },
    {
        'title':    'First Aid for Severe Bleeding',
        'category': 'bleeding',
        'severity': 'emergency',
        'steps': [
            'Call emergency services (999 / 112) if the bleeding is severe.',
            'Put on gloves or use a barrier if available to protect yourself.',
            'Apply firm, direct pressure to the wound using a clean cloth or bandage.',
            'Do NOT remove the cloth if it becomes soaked — add more material on top.',
            'If possible, raise the injured limb above the level of the heart.',
            'Maintain firm pressure continuously for at least 10–15 minutes.',
            'Keep the person warm and calm; treat for shock if necessary (lay flat, elevate legs).',
        ],
        'warnings': 'Do NOT remove objects embedded in a wound — stabilise them in place. Do NOT apply a tourniquet unless trained and bleeding is catastrophic.',
    },
    {
        'title':    'First Aid for Fainting',
        'category': 'fainting',
        'severity': 'moderate',
        'steps': [
            'If the person feels faint, have them sit or lie down immediately before they fall.',
            'If they have fainted, lay them on their back on a flat surface.',
            'Raise their legs 20–30 cm above the level of the heart to restore blood flow to the brain.',
            'Loosen any tight clothing around the neck, chest, or waist.',
            'Check for breathing and a pulse. If absent, begin CPR.',
            'Once they recover, have them sit up slowly to avoid fainting again.',
            'Give them water to sip once fully conscious.',
        ],
        'warnings': 'Seek immediate medical attention if the person does not regain consciousness within 1 minute, has chest pain, is pregnant, or is diabetic.',
    },
    {
        'title':    'First Aid for Fractures (Suspected Broken Bone)',
        'category': 'fractures',
        'severity': 'urgent',
        'steps': [
            'Do not move the person if you suspect a serious fracture, especially of the spine or neck.',
            'Call emergency services if the fracture is severe, involves the spine, or the bone is visible.',
            'Immobilise the injured area in the position found — do not try to realign it.',
            'Apply a makeshift splint if available: pad with clothing and tie above and below the break.',
            'Apply an ice pack wrapped in cloth to reduce swelling — never apply ice directly to skin.',
            'Elevate the limb if possible and if it does not cause pain.',
            'Monitor for signs of shock (pale skin, rapid breathing, confusion) and treat accordingly.',
        ],
        'warnings': 'Never attempt to straighten a broken bone. For open fractures where bone is visible, cover with a clean dressing without pressure and seek emergency care immediately.',
    },
]


# ── Seed function with fix for Render ─────────────────────────────────────────
def seed():
    with app.app_context():
        # Create instance directory if it doesn't exist
        os.makedirs('instance', exist_ok=True)
        
        # Check if data already exists
        try:
            existing_count = Symptom.query.count()
            if existing_count > 0:
                print(f"Database already has {existing_count} symptoms. Skipping seed.")
                print("To re-seed, delete instance/medassist.db and redeploy.")
                return
        except Exception as e:
            print(f"Creating new database...")
        
        print('Dropping existing tables...')
        db.drop_all()

        print('Creating fresh tables...')
        db.create_all()

        # Seed Symptoms
        sym_map = {}
        for s_data in SYMPTOMS:
            obj = Symptom(**s_data)
            db.session.add(obj)
            sym_map[s_data['slug']] = obj
        db.session.flush()
        print(f'  ✓ Symptoms seeded ({len(SYMPTOMS)} records)')

        # Seed Conditions + attach Symptoms
        for c_data in CONDITIONS:
            slugs = c_data.pop('symptom_slugs')
            obj = Condition(**c_data)
            obj.symptoms = [sym_map[sl] for sl in slugs if sl in sym_map]
            db.session.add(obj)
        db.session.flush()
        print(f'  ✓ Conditions seeded ({len(CONDITIONS)} records)')

        # Seed Questions
        for q_data in QUESTIONS:
            opts = q_data.pop('options')
            obj = Question(options_json=json.dumps(opts), **q_data)
            db.session.add(obj)
        db.session.flush()
        print(f'  ✓ Questions seeded ({len(QUESTIONS)} records)')

        # Seed First Aid Guides
        for g_data in FIRST_AID_GUIDES:
            steps = g_data.pop('steps')
            obj = FirstAidGuide(steps_json=json.dumps(steps), **g_data)
            db.session.add(obj)

        db.session.commit()
        print(f'  ✓ First aid guides seeded ({len(FIRST_AID_GUIDES)} records)')
        print('\nDone! Database ready at instance/medassist.db')


if __name__ == '__main__':
    seed()