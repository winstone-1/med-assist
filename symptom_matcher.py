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


# Pregnancy-specific symptom mapping
PREGNANCY_SYMPTOM_MAP = {
    'severe headache': 'headache',
    'headache': 'headache',
    'swelling': 'swelling',
    'vision changes': 'vision-changes',
    'blurred vision': 'vision-changes',
    'spots in vision': 'vision-changes',
    'decreased fetal movement': 'decreased-fetal-movement',
    'nausea': 'nausea',
    'vomiting': 'vomiting',
    'dizziness': 'dizziness',
    'fatigue': 'fatigue',
    'abdominal pain': 'abdominal-pain',
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

    for key, value in answers.items():
        if not value:
            continue

        # Normalise value to a list
        if isinstance(value, list):
            values = value
        elif isinstance(value, str):
            # Check if it's a comma-separated string
            if ',' in value:
                values = [v.strip() for v in value.split(',')]
            else:
                values = [value]
        else:
            values = [str(value)]

        # Handle question keys (q_1, q_2, q_3, q_4, or dynamic IDs)
        # Extract question number from key (e.g., 'q_1' -> 1, 'q_12' -> 12)
        q_num = None
        if key.startswith('q_'):
            try:
                q_num = int(key.split('_')[1])
            except (IndexError, ValueError):
                q_num = None

        # Q1 — symptoms checkbox (or any checkbox with symptom names)
        if q_num == 1 or key == 'q_1' or 'symptom' in str(values).lower():
            for v in values:
                v_clean = v.strip().lower().replace(' ', '-')
                # Map pregnancy-specific terms
                v_clean = PREGNANCY_SYMPTOM_MAP.get(v_clean, v_clean)
                symptom_slugs.add(v_clean)

        # Q2 — duration radio
        elif q_num == 2 or key == 'q_2' or 'long' in key.lower():
            if values:
                duration = values[0].strip()

        # Q3 — severity radio
        elif q_num == 3 or key == 'q_3' or 'severe' in key.lower() or 'severity' in key.lower():
            if values:
                severity_level = values[0].strip()

        # Q4 — risk factors checkbox
        elif q_num == 4 or key == 'q_4' or 'risk' in key.lower() or 'high-risk' in key.lower():
            for v in values:
                risk_factors.append(v.strip())

        # Fallback for any other checkbox (assume it's symptoms)
        elif 'checkbox' in str(key).lower() or 'option' in str(key).lower():
            for v in values:
                v_clean = v.strip().lower().replace(' ', '-')
                symptom_slugs.add(v_clean)

    print(f"[DEBUG] Symptom slugs: {symptom_slugs}")
    print(f"[DEBUG] Duration: {duration}")
    print(f"[DEBUG] Severity: {severity_level}")
    print(f"[DEBUG] Risk factors: {risk_factors}")

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

    if not symptom_slugs:
        print("[DEBUG] No symptoms found - returning empty list")
        return []

    conditions = Condition.query.all()
    print(f"[DEBUG] Total conditions in DB: {len(conditions)}")

    results = []

    for cond in conditions:
        cond_slugs = {s.slug for s in cond.symptoms}

        if not cond_slugs:
            continue

        # Base score: symptom overlap
        matched    = cond_slugs & symptom_slugs
        base_score = len(matched) / len(cond_slugs)

        print(f"[DEBUG] {cond.name} | cond_slugs={cond_slugs} | matched={matched} | score={base_score:.2f}")

        if base_score < threshold:
            continue

        # Duration modifier
        duration_mod = DURATION_WEIGHT.get(duration, 1.0)

        # User severity modifier
        severity_mod = USER_SEVERITY_WEIGHT.get(severity_level, 1.0)

        # Risk factor bonus
        risk_bonus = 0.0
        if risk_factors and 'None of the above' not in risk_factors:
            # Check for pregnancy (regardless of exact phrasing)
            is_pregnant = False
            for rf in risk_factors:
                if 'pregnant' in rf.lower():
                    is_pregnant = True
                    break
            
            if is_pregnant:
                risk_bonus = 0.3
                # Special boost for pre-eclampsia symptoms
                if cond.name == 'Pre-eclampsia' and {'headache', 'vision-changes', 'swelling'} & symptom_slugs:
                    risk_bonus += 0.2
            else:
                risk_bonus = 0.1 * len(risk_factors)

        # Final score
        final_score = (base_score * duration_mod * severity_mod) + risk_bonus

        results.append({
            'condition':   cond,
            'base_score':  round(base_score,  2),
            'final_score': round(final_score, 2),
            'matched':     sorted(list(matched)),
            'severity':    cond.severity,
            'guide':       cond.firstaid_guide,
        })

    # Sort: final_score DESC, then severity weight DESC
    results.sort(key=lambda x: (
        -x['final_score'],
        -SEVERITY_WEIGHT.get(x['severity'], 0)
    ))

    print(f"[DEBUG] Final results count: {len(results)}")
    
    # If no results, return empty list
    return results


def check_pre_eclampsia(answers: dict) -> dict:
    """
    Special check for pre-eclampsia in pregnant women.
    Returns emergency result if symptoms match.
    """
    parsed = parse_answers(answers)
    symptom_slugs = parsed['symptom_slugs']
    risk_factors = parsed['risk_factors']
    
    # Check if pregnant
    is_pregnant = False
    for rf in risk_factors:
        if 'pregnant' in rf.lower():
            is_pregnant = True
            break
    
    if not is_pregnant:
        return None
    
    # Pre-eclampsia key symptoms
    pre_eclampsia_symptoms = {
        'headache', 'vision-changes', 'swelling', 
        'abdominal-pain', 'dizziness', 'nausea'
    }
    
    has_key_symptoms = len(pre_eclampsia_symptoms & symptom_slugs) >= 2
    has_severe_headache = 'headache' in symptom_slugs
    
    if is_pregnant and (has_key_symptoms or has_severe_headache):
        # Try to find pre-eclampsia in database
        pre_eclampsia = Condition.query.filter(
            Condition.name.ilike('%pre-eclampsia%')
        ).first()
        
        if pre_eclampsia:
            matched = list(pre_eclampsia_symptoms & symptom_slugs)
            return {
                'condition': pre_eclampsia,
                'base_score': 0.95,
                'final_score': 1.5,
                'matched': matched if matched else ['headache'],
                'severity': 'emergency',
                'guide': pre_eclampsia.firstaid_guide
            }
    return None


def get_severity_label(severity: str) -> dict:
    labels = {
        'low':       {'label': 'Low',       'color': 'success', 'icon': '🟢'},
        'moderate':  {'label': 'Moderate',  'color': 'warning', 'icon': '🟡'},
        'urgent':    {'label': 'Urgent',    'color': 'orange',  'icon': '🟠'},
        'emergency': {'label': 'Emergency', 'color': 'danger',  'icon': '🔴'},
    }
    return labels.get(severity, {'label': severity, 'color': 'secondary', 'icon': '⚪'})