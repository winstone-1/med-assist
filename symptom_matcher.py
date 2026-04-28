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

        # question 1 — symptoms (checkbox, comma separated)
        if key == 'q_1':
            values = value if isinstance(value, list) else value.split(',')
            for v in values:
                slug = v.strip().lower().replace(' ', '-')
                symptom_slugs.add(slug)

        # question 2 — duration (radio)
        elif key == 'q_2':
            duration = value.strip()

        # question 3 — severity self-assessment (radio)
        elif key == 'q_3':
            severity_level = value.strip()

        # question 4 — risk factors (checkbox)
        elif key == 'q_4':
            values = value if isinstance(value, list) else value.split(',')
            risk_factors = [v.strip() for v in values]

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
        return []

    conditions = Condition.query.all()
    results    = []

    for cond in conditions:
        cond_slugs = {s.slug for s in cond.symptoms}

        if not cond_slugs:
            continue

        # ── Base score: symptom overlap ──────────────────────────────────────
        matched     = cond_slugs & symptom_slugs
        base_score  = len(matched) / len(cond_slugs)

        if base_score < threshold:
            continue

        # ── Duration modifier ────────────────────────────────────────────────
        duration_mod = DURATION_WEIGHT.get(duration, 1.0)

        # ── User severity modifier ───────────────────────────────────────────
        severity_mod = USER_SEVERITY_WEIGHT.get(severity_level, 1.0)

        # ── Risk factor bonus ────────────────────────────────────────────────
        risk_bonus = 0.0
        if risk_factors and 'None of the above' not in risk_factors:
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