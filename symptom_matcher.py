# symptom_matcher.py
from models import Symptom, Condition


SEVERITY_WEIGHT = {
    'emergency': 4,
    'urgent':    3,
    'moderate':  2,
    'low':       1,
}


DURATION_WEIGHT = {
    'Less than 24 hours': 0.8,
    '1–3 days':           1.0,
    '4–7 days':           1.2,
    'More than a week':   1.4,
}


USER_SEVERITY_WEIGHT = {
    'Mild — I can manage daily activities':        0.8,
    'Moderate — I am struggling with some activities': 1.0,
    'Severe — I cannot do daily activities':       1.2,
    'Critical — I need immediate help':            1.5,
}


# Pregnancy-specific symptom mapping (for when q_1 is dynamic)
PREGNANCY_SYMPTOMS_MAP = {
    'severe headache': 'severe-headache',
    'headache': 'headache',
    'sudden swelling': 'sudden-swelling',
    'swelling face': 'swelling-face',
    'swelling hands': 'swelling-hands',
    'vision changes': 'vision-changes',
    'blurred vision': 'blurred-vision',
    'spots in vision': 'spots-in-vision',
    'decreased fetal movement': 'decreased-fetal-movement',
    'nausea': 'nausea',
    'vomiting': 'vomiting',
    'dizziness': 'dizziness',
    'fatigue': 'fatigue',
    'abdominal pain': 'abdominal-pain',
    'upper right abdominal pain': 'upper-right-abdominal-pain',
}


def parse_answers(answers: dict) -> dict:
    """
    Parse raw session answers into structured data.
    Returns dict with symptom_slugs, duration, severity_level, risk_factors.
    """
    symptom_slugs  = set()
    duration       = None
    severity_level = None
    risk_factors   = []
    weeks_pregnant = None

    for key, value in answers.items():
        if not value:
            continue

        # Handle all question types (q_1, q_2, q_3, q_4, or dynamic q_id)
        # Convert value to list if it's a string with commas
        if isinstance(value, str) and ',' in value and 'checkbox' in str(key):
            value = [v.strip() for v in value.split(',')]

        # SYMPTOMS - Question 1 or any checkbox with symptom names
        if key == 'q_1' or (key.startswith('q_') and 'symptom' in str(value).lower()) or 'checkbox' in str(key):
            values = value if isinstance(value, list) else [value]
            for v in values:
                v_clean = v.strip().lower()
                # Map to slug
                slug = PREGNANCY_SYMPTOMS_MAP.get(v_clean, v_clean.replace(' ', '-'))
                symptom_slugs.add(slug)

        # DURATION - Question 2
        elif key == 'q_2' or 'duration' in key.lower() or 'long' in key.lower():
            duration = value.strip()

        # SEVERITY - Question 3
        elif key == 'q_3' or 'severity' in key.lower():
            severity_level = value.strip()

        # RISK FACTORS - Question 4 (pregnancy, age, etc.)
        elif key == 'q_4' or 'risk' in key.lower() or 'pregnant' in key.lower():
            values = value if isinstance(value, list) else [value]
            for v in values:
                v_clean = v.strip()
                risk_factors.append(v_clean)
                if 'pregnant' in v_clean.lower():
                    # Check if weeks were provided elsewhere
                    pass

        # Pregnancy weeks (custom field)
        elif 'weeks' in key.lower() or 'pregnancy' in key.lower():
            try:
                weeks_pregnant = int(value)
            except:
                pass

    # If pregnant, add pregnancy as a risk factor
    if weeks_pregnant or 'pregnant' in str(risk_factors).lower():
        risk_factors.append('Pregnant')

    return {
        'symptom_slugs':  symptom_slugs,
        'duration':       duration,
        'severity_level': severity_level,
        'risk_factors':   risk_factors,
    }


def match_symptoms(answers: dict, threshold: float = 0.25) -> list:
    """
    Core matching engine.
    Scores each condition based on:
      - symptom overlap ratio
      - duration modifier
      - user severity modifier
      - risk factor bonus
      - condition severity weight

    Returns list of result dicts sorted by final_score DESC.
    """
    parsed         = parse_answers(answers)
    symptom_slugs  = parsed['symptom_slugs']
    duration       = parsed['duration']
    severity_level = parsed['severity_level']
    risk_factors   = parsed['risk_factors']

    # Debug print to see what's being passed
    print(f"[DEBUG] Symptom slugs: {symptom_slugs}")
    print(f"[DEBUG] Duration: {duration}")
    print(f"[DEBUG] Severity: {severity_level}")
    print(f"[DEBUG] Risk factors: {risk_factors}")

    if not symptom_slugs:
        print("[DEBUG] No symptoms found - returning empty list")
        return []

    conditions = Condition.query.all()
    print(f"[DEBUG] Total conditions in DB: {len(conditions)}")
    
    results    = []

    for cond in conditions:
        cond_slugs = {s.slug for s in cond.symptoms}
        
        print(f"[DEBUG] Condition: {cond.name}, slugs: {cond_slugs}")

        if not cond_slugs:
            continue

        # ── Base score: symptom overlap ──────────────────────────────────────
        matched     = cond_slugs & symptom_slugs
        base_score  = len(matched) / len(cond_slugs)

        print(f"[DEBUG] Matched: {matched}, base_score: {base_score}")

        if base_score < threshold:
            continue

        # ── Duration modifier ────────────────────────────────────────────────
        duration_mod = DURATION_WEIGHT.get(duration, 1.0)

        # ── User severity modifier ───────────────────────────────────────────
        severity_mod = USER_SEVERITY_WEIGHT.get(severity_level, 1.0)

        # ── Risk factor bonus ────────────────────────────────────────────────
        risk_bonus = 0.0
        if risk_factors and 'None of the above' not in risk_factors:
            # Higher bonus for pregnancy risk
            if 'Pregnant' in risk_factors:
                risk_bonus = 0.3
            else:
                risk_bonus = 0.1 * len(risk_factors)

        # ── Final score ──────────────────────────────────────────────────────
        final_score = (base_score * duration_mod * severity_mod) + risk_bonus

        results.append({
            'condition':   cond,
            'base_score':  round(base_score,  2),
            'final_score': round(final_score, 2),
            'matched':     sorted(list(matched)),
            'severity':    cond.severity,
            'guide':       cond.firstaid_guide,
        })

    # ── Sort: final_score DESC, then severity weight DESC ────────────────────
    results.sort(key=lambda x: (
        -x['final_score'],
        -SEVERITY_WEIGHT.get(x['severity'], 0)
    ))

    print(f"[DEBUG] Final results count: {len(results)}")
    return results


def get_severity_label(severity: str) -> dict:
    """
    Returns display label and Bootstrap color class for a severity level.
    """
    labels = {
        'low':       {'label': 'Low',       'color': 'success', 'icon': '🟢'},
        'moderate':  {'label': 'Moderate',  'color': 'warning', 'icon': '🟡'},
        'urgent':    {'label': 'Urgent',    'color': 'orange',  'icon': '🟠'},
        'emergency': {'label': 'Emergency', 'color': 'danger',  'icon': '🔴'},
    }
    return labels.get(severity, {'label': severity, 'color': 'secondary', 'icon': '⚪'})


# Pre-eclampsia specific check (for high accuracy)
def check_pre_eclampsia(answers: dict) -> dict:
    """
    Special check for pre-eclampsia in pregnant women.
    Returns emergency result if symptoms match.
    """
    parsed = parse_answers(answers)
    symptom_slugs = parsed['symptom_slugs']
    risk_factors = parsed['risk_factors']
    
    # Pre-eclampsia key symptoms
    pre_eclampsia_symptoms = {
        'severe-headache', 'vision-changes', 'blurred-vision', 
        'spots-in-vision', 'sudden-swelling', 'swelling-face',
        'swelling-hands', 'upper-right-abdominal-pain'
    }
    
    # Check if pregnant and has key symptoms
    is_pregnant = 'Pregnant' in risk_factors or any('pregnant' in str(r).lower() for r in risk_factors)
    has_key_symptoms = len(pre_eclampsia_symptoms & symptom_slugs) >= 2
    
    if is_pregnant and has_key_symptoms:
        from models import Condition
        pre_eclampsia = Condition.query.filter(
            Condition.name.ilike('%pre-eclampsia%')
        ).first()
        
        if pre_eclampsia:
            return {
                'condition': pre_eclampsia,
                'base_score': 0.95,
                'final_score': 1.5,
                'matched': list(pre_eclampsia_symptoms & symptom_slugs),
                'severity': 'emergency',
                'guide': pre_eclampsia.firstaid_guide
            }
    return None