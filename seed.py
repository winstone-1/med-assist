# seed.py
import json
import os
import sys

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, Symptom, Condition, Question, FirstAidGuide

# Create instance directory FIRST before anything else
os.makedirs('instance', exist_ok=True)

app = create_app()

# ── Symptoms ─────────────────────────────────────────────────────────────────
SYMPTOMS = [
    {'name': 'Fever', 'slug': 'fever', 'body_area': 'systemic', 'description': 'Elevated body temperature above 38°C'},
    {'name': 'Headache', 'slug': 'headache', 'body_area': 'head', 'description': 'Pain or pressure in the head'},
    {'name': 'Cough', 'slug': 'cough', 'body_area': 'respiratory', 'description': 'Sudden expulsion of air from the lungs'},
    {'name': 'Sore Throat', 'slug': 'sore-throat', 'body_area': 'throat', 'description': 'Pain or irritation in the throat'},
    {'name': 'Fatigue', 'slug': 'fatigue', 'body_area': 'systemic', 'description': 'Extreme tiredness and lack of energy'},
    {'name': 'Nausea', 'slug': 'nausea', 'body_area': 'abdomen', 'description': 'Feeling of sickness with an inclination to vomit'},
    {'name': 'Vomiting', 'slug': 'vomiting', 'body_area': 'abdomen', 'description': 'Forceful expulsion of stomach contents'},
    {'name': 'Diarrhoea', 'slug': 'diarrhoea', 'body_area': 'abdomen', 'description': 'Loose or watery stools'},
    {'name': 'Abdominal Pain', 'slug': 'abdominal-pain', 'body_area': 'abdomen', 'description': 'Pain in the stomach area'},
    {'name': 'Chest Pain', 'slug': 'chest-pain', 'body_area': 'chest', 'description': 'Pain or tightness in the chest'},
    {'name': 'Shortness of Breath', 'slug': 'shortness-of-breath', 'body_area': 'chest', 'description': 'Difficulty breathing'},
    {'name': 'Dizziness', 'slug': 'dizziness', 'body_area': 'head', 'description': 'Feeling faint or lightheaded'},
    {'name': 'Rash', 'slug': 'rash', 'body_area': 'skin', 'description': 'Skin irritation or redness'},
    {'name': 'Runny Nose', 'slug': 'runny-nose', 'body_area': 'head', 'description': 'Excess nasal discharge'},
    {'name': 'Body Aches', 'slug': 'body-aches', 'body_area': 'systemic', 'description': 'General muscle pain'},
    {'name': 'Loss of Appetite', 'slug': 'loss-of-appetite', 'body_area': 'systemic', 'description': 'Reduced desire to eat'},
    {'name': 'Sweating', 'slug': 'sweating', 'body_area': 'systemic', 'description': 'Excessive perspiration'},
    {'name': 'Chills', 'slug': 'chills', 'body_area': 'systemic', 'description': 'Feeling of coldness with shivering'},
    {'name': 'Swollen Lymph Nodes', 'slug': 'swollen-lymph-nodes', 'body_area': 'throat', 'description': 'Enlarged glands'},
    {'name': 'Eye Redness', 'slug': 'eye-redness', 'body_area': 'head', 'description': 'Red or irritated eyes'},
]

# ── Conditions (UPDATED with Pregnancy Conditions) ────────────────────────────
CONDITIONS = [
    # Existing Conditions
    {
        'name': 'Common Cold',
        'severity': 'low',
        'description': 'A viral infection of the upper respiratory tract. Usually harmless and resolves within 7–10 days.',
        'when_to_see_doctor': 'If symptoms last more than 10 days, worsen after improving, or include high fever above 39°C.',
        'symptom_slugs': ['runny-nose', 'sore-throat', 'cough', 'headache', 'fatigue', 'fever'],
    },
    {
        'name': 'Influenza (Flu)',
        'severity': 'moderate',
        'description': 'A contagious respiratory illness caused by influenza viruses. More severe than a cold with sudden onset.',
        'when_to_see_doctor': 'If you have difficulty breathing, persistent chest pain, severe vomiting, or are in a high-risk group.',
        'symptom_slugs': ['fever', 'chills', 'body-aches', 'headache', 'fatigue', 'cough', 'sore-throat', 'loss-of-appetite'],
    },
    {
        'name': 'Gastroenteritis (Stomach Flu)',
        'severity': 'moderate',
        'description': 'Inflammation of the stomach and intestines, usually caused by a viral or bacterial infection.',
        'when_to_see_doctor': 'If diarrhoea contains blood, vomiting persists more than 2 days, or signs of dehydration appear.',
        'symptom_slugs': ['nausea', 'vomiting', 'diarrhoea', 'abdominal-pain', 'fever', 'loss-of-appetite'],
    },
    {
        'name': 'Strep Throat',
        'severity': 'moderate',
        'description': 'A bacterial throat infection caused by Streptococcus. Requires antibiotic treatment.',
        'when_to_see_doctor': 'See a doctor promptly — strep requires antibiotics.',
        'symptom_slugs': ['sore-throat', 'fever', 'swollen-lymph-nodes', 'headache', 'loss-of-appetite'],
    },
    {
        'name': 'Malaria',
        'severity': 'urgent',
        'description': 'A serious mosquito-borne disease common in tropical regions. Requires immediate treatment.',
        'when_to_see_doctor': 'Seek medical attention immediately if malaria is suspected.',
        'symptom_slugs': ['fever', 'chills', 'sweating', 'headache', 'nausea', 'vomiting', 'body-aches', 'fatigue'],
    },
    {
        'name': 'Typhoid Fever',
        'severity': 'urgent',
        'description': 'A bacterial infection caused by Salmonella typhi. Common in areas with poor sanitation.',
        'when_to_see_doctor': 'Seek medical care immediately — typhoid needs antibiotics.',
        'symptom_slugs': ['fever', 'headache', 'abdominal-pain', 'loss-of-appetite', 'fatigue', 'rash'],
    },
    {
        'name': 'Heart Attack',
        'severity': 'emergency',
        'description': 'A blockage of blood flow to the heart muscle. Every minute without treatment causes damage.',
        'when_to_see_doctor': 'Call emergency services (999/112) IMMEDIATELY.',
        'symptom_slugs': ['chest-pain', 'shortness-of-breath', 'nausea', 'sweating', 'dizziness', 'fatigue'],
    },
    {
        'name': 'Allergic Reaction',
        'severity': 'urgent',
        'description': 'An immune system response to a foreign substance.',
        'when_to_see_doctor': 'Seek emergency care if throat swelling or difficulty breathing occurs.',
        'symptom_slugs': ['rash', 'shortness-of-breath', 'nausea', 'dizziness', 'eye-redness'],
    },
    
    # ========== NEW PREGNANCY CONDITIONS ==========
    
    {
        'name': 'Pre-eclampsia',
        'severity': 'emergency',
        'description': 'A serious pregnancy complication characterized by high blood pressure and signs of organ damage. Can progress to eclampsia (seizures) if untreated.',
        'when_to_see_doctor': 'CALL 999 IMMEDIATELY. This is a medical emergency. Go to hospital now.',
        'symptom_slugs': ['headache', 'nausea', 'vomiting', 'dizziness', 'abdominal-pain'],
    },
    {
        'name': 'Hyperemesis Gravidarum',
        'severity': 'urgent',
        'description': 'Severe, persistent nausea and vomiting during pregnancy that can lead to dehydration, weight loss, and electrolyte imbalance.',
        'when_to_see_doctor': 'Contact your OB/GYN today. You may need IV fluids and anti-nausea medication.',
        'symptom_slugs': ['nausea', 'vomiting', 'dizziness', 'fatigue', 'loss-of-appetite'],
    },
    {
        'name': 'Urinary Tract Infection (UTI) in Pregnancy',
        'severity': 'urgent',
        'description': 'A bacterial infection in the urinary system. During pregnancy, UTIs can lead to kidney infections and preterm labor if untreated.',
        'when_to_see_doctor': 'Contact your OB/GYN today for a urine test. Antibiotics are safe during pregnancy.',
        'symptom_slugs': ['abdominal-pain', 'fever', 'nausea', 'fatigue'],
    },
    {
        'name': 'Anemia in Pregnancy',
        'severity': 'moderate',
        'description': 'Iron deficiency during pregnancy. Common but can cause fatigue, weakness, and complications if severe.',
        'when_to_see_doctor': 'Request a blood test at your next prenatal visit. Iron supplements may be needed.',
        'symptom_slugs': ['fatigue', 'dizziness', 'headache', 'shortness-of-breath'],
    },
    {
        'name': 'Gestational Diabetes',
        'severity': 'moderate',
        'description': 'High blood sugar that develops during pregnancy. Usually manageable with diet and monitoring.',
        'when_to_see_doctor': 'Schedule glucose tolerance test. Monitor blood sugar as directed.',
        'symptom_slugs': ['fatigue', 'nausea', 'frequent-urination', 'excessive-thirst'],
    },
    {
        'name': 'Placenta Previa',
        'severity': 'emergency',
        'description': 'A condition where the placenta covers the cervix, causing painless bleeding in the third trimester.',
        'when_to_see_doctor': 'CALL 999 IMMEDIATELY. Go to hospital now. Do NOT have a vaginal exam.',
        'symptom_slugs': ['abdominal-pain', 'dizziness', 'fatigue'],
    },
    {
        'name': 'Preterm Labor',
        'severity': 'emergency',
        'description': 'Regular contractions and cervical changes before 37 weeks of pregnancy.',
        'when_to_see_doctor': 'CALL 999 IMMEDIATELY. Go to Labor & Delivery triage.',
        'symptom_slugs': ['abdominal-pain', 'back-pain', 'pelvic-pressure'],
    },
    {
        'name': 'Pneumonia in Pregnancy',
        'severity': 'urgent',
        'description': 'Lung infection that can be more severe during pregnancy due to immune system changes.',
        'when_to_see_doctor': 'Seek medical care today. Pneumonia requires prompt treatment.',
        'symptom_slugs': ['fever', 'cough', 'chest-pain', 'shortness-of-breath', 'fatigue', 'chills', 'sweating'],
    },
]

# ── Questions (UPDATED with Pregnancy Option) ─────────────────────────────────
QUESTIONS = [
    {
        'text': 'Which of the following symptoms are you currently experiencing? (Select all that apply)',
        'question_type': 'checkbox',
        'order': 1,
        'options': ['Fever', 'Headache', 'Cough', 'Sore Throat', 'Fatigue', 'Nausea', 'Vomiting', 'Diarrhoea', 'Abdominal Pain', 'Chest Pain', 'Shortness of Breath', 'Dizziness', 'Rash', 'Runny Nose', 'Body Aches', 'Loss of Appetite', 'Sweating', 'Chills', 'Swollen Lymph Nodes', 'Eye Redness'],
    },
    {
        'text': 'How long have you been experiencing these symptoms?',
        'question_type': 'radio',
        'order': 2,
        'options': ['Less than 24 hours', '1–3 days', '4–7 days', 'More than a week'],
    },
    {
        'text': 'How would you describe the overall severity of your symptoms?',
        'question_type': 'radio',
        'order': 3,
        'options': ['Mild — I can manage daily activities', 'Moderate — I am struggling with some activities', 'Severe — I cannot do daily activities', 'Critical — I need immediate help'],
    },
    {
        'text': 'Do you have any of the following high-risk factors?',
        'question_type': 'checkbox',
        'order': 4,
        'options': ['I am over 60 years old', 'I have a chronic illness (diabetes, heart disease, etc.)', 'I am pregnant', 'I have a weakened immune system', 'None of the above'],
    },
]

# ── First Aid Guides (UPDATED with Pregnancy) ─────────────────────────────────
FIRST_AID_GUIDES = [
    {
        'title': 'First Aid for Choking (Adult)',
        'category': 'choking',
        'severity': 'emergency',
        'steps': ['Ask loudly: "Are you choking?"', 'Call emergency services (999/112).', 'Give 5 back blows between shoulder blades.', 'Give 5 abdominal thrusts (Heimlich).', 'Alternate until object is cleared.'],
        'warnings': 'Do NOT perform on infants or pregnant women.',
    },
    {
        'title': 'First Aid for Burns (Minor)',
        'category': 'burns',
        'severity': 'moderate',
        'steps': ['Cool under running water for 20 minutes.', 'Remove jewellery near the burn.', 'Cover with sterile dressing.'],
        'warnings': 'Do NOT apply ice, butter, or toothpaste.',
    },
    {
        'title': 'First Aid for Severe Bleeding',
        'category': 'bleeding',
        'severity': 'emergency',
        'steps': ['Call emergency services.', 'Apply firm direct pressure.', 'Raise injured limb if possible.', 'Keep pressure until help arrives.'],
        'warnings': 'Do NOT remove embedded objects.',
    },
    {
        'title': 'First Aid for Fainting',
        'category': 'fainting',
        'severity': 'moderate',
        'steps': ['Lay person on their back.', 'Raise legs 20-30cm.', 'Loosen tight clothing.', 'Check breathing.'],
        'warnings': 'Seek help if not conscious within 1 minute.',
    },
    {
        'title': 'First Aid for Fractures',
        'category': 'fractures',
        'severity': 'urgent',
        'steps': ['Do not move the person.', 'Immobilise the injured area.', 'Apply ice pack wrapped in cloth.', 'Seek medical attention.'],
        'warnings': 'Never try to straighten a broken bone.',
    },
    {
        'title': 'Emergency Guide: Pre-eclampsia',
        'category': 'pregnancy',
        'severity': 'emergency',
        'steps': ['CALL 999 IMMEDIATELY', 'Go to the nearest Emergency Room', 'Lie on your left side', 'Do not take any medication', 'Inform medical staff you are pregnant and symptoms started suddenly'],
        'warnings': 'Pre-eclampsia can progress to seizures. DO NOT wait to see if symptoms improve.',
    },
    {
        'title': 'Guide: Hyperemesis Gravidarum',
        'category': 'pregnancy',
        'severity': 'urgent',
        'steps': ['Contact your OB/GYN today', 'Try small, frequent meals every 2 hours', 'Stay hydrated with small sips of water or electrolyte drinks', 'Avoid triggers (strong smells, fatty foods)', 'Monitor for dark urine (dehydration sign)'],
        'warnings': 'If you cannot keep any fluids down for 12 hours, go to the hospital.',
    },
    {
        'title': 'Guide: UTI in Pregnancy',
        'category': 'pregnancy',
        'severity': 'urgent',
        'steps': ['Drink plenty of water (8-10 glasses daily)', 'Contact OB/GYN for urine test', 'Take prescribed antibiotics as directed', 'Avoid caffeine and sugary drinks', 'Urinate frequently, don\'t hold it'],
        'warnings': 'Untreated UTI can lead to kidney infection and preterm labor.',
    },
]


def seed():
    with app.app_context():
        print('Creating database tables...')
        db.create_all()
        
        # Check if already seeded
        if Symptom.query.count() > 0:
            print(f'Database already has {Symptom.query.count()} symptoms. Skipping seed.')
            return

        # Seed Symptoms
        sym_map = {}
        for s_data in SYMPTOMS:
            obj = Symptom(**s_data)
            db.session.add(obj)
            sym_map[s_data['slug']] = obj
        db.session.commit()
        print(f'Seeded {len(SYMPTOMS)} symptoms')

        # Seed Conditions
        for c_data in CONDITIONS:
            slugs = c_data.pop('symptom_slugs')
            obj = Condition(**c_data)
            obj.symptoms = [sym_map[sl] for sl in slugs if sl in sym_map]
            db.session.add(obj)
        db.session.commit()
        print(f'Seeded {len(CONDITIONS)} conditions')

        # Seed Questions
        for q_data in QUESTIONS:
            opts = q_data.pop('options')
            obj = Question(options_json=json.dumps(opts), **q_data)
            db.session.add(obj)
        db.session.commit()
        print(f'Seeded {len(QUESTIONS)} questions')

        # Seed First Aid Guides
        for g_data in FIRST_AID_GUIDES:
            steps = g_data.pop('steps')
            obj = FirstAidGuide(steps_json=json.dumps(steps), **g_data)
            db.session.add(obj)
        db.session.commit()
        print(f'Seeded {len(FIRST_AID_GUIDES)} first aid guides')
        
        print('Database seeding completed successfully!')


if __name__ == '__main__':
    seed()
    print('Done!')