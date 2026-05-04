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
    'Mild — I can manage daily activities':                    0.8,
    'Moderate — I am struggling with some activities':         1.0,
    'Severe — I cannot do daily activities':                   1.2,
    'Critical — I need immediate help':                        1.5,
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
            values = [value]
        else:
            values = [str(value)]

        # Q1 — symptoms checkbox
        if key == 'q_1':
            for v in values:
                slug = v.strip().lower().replace(' ', '-')
                symptom_slugs.add(slug)

        # Q2 — duration radio
        elif key == 'q_2':
            duration = values[0].strip()

        # Q3 — severity radio
        elif key == 'q_3':
            severity_level = values[0].strip()

        # Q4 — risk factors checkbox
        elif key == 'q_4':
            for v in values:
                risk_factors.append(v.strip())

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
            if any('pregnant' in r.lower() for r in risk_factors):
                risk_bonus = 0.3
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
    return results


def get_severity_label(severity: str) -> dict:
    labels = {
        'low':       {'label': 'Low',       'color': 'success', 'icon': '🟢'},
        'moderate':  {'label': 'Moderate',  'color': 'warning', 'icon': '🟡'},
        'urgent':    {'label': 'Urgent',    'color': 'orange',  'icon': '🟠'},
        'emergency': {'label': 'Emergency', 'color': 'danger',  'icon': '🔴'},
    }
    return labels.get(severity, {'label': severity, 'color': 'secondary', 'icon': '⚪'})