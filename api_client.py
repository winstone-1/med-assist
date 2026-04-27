# api_client.py
import requests

OPENFDA_BASE_URL = "https://api.fda.gov/drug"

# ── Map our conditions to relevant drug search terms ─────────────────────────
CONDITION_DRUG_MAP = {
    'Common Cold':                 'cold',
    'Influenza (Flu)':             'influenza',
    'Gastroenteritis (Stomach Flu)': 'gastroenteritis',
    'Strep Throat':                'streptococcal',
    'Malaria':                     'malaria',
    'Typhoid Fever':               'typhoid',
    'Heart Attack':                'cardiac',
    'Allergic Reaction':           'allergy',
}


def get_drug_warnings(condition_name: str) -> list:
    """
    Fetch drug warnings from OpenFDA related to a condition.
    Returns a list of warning dicts with brand_name and warnings.
    """
    search_term = CONDITION_DRUG_MAP.get(condition_name, condition_name)

    try:
        response = requests.get(
            f"{OPENFDA_BASE_URL}/label.json",
            params={
                'search': f'indications_and_usage:"{search_term}"',
                'limit':  3,
            },
            timeout=5
        )

        if response.status_code != 200:
            return []

        data    = response.json()
        results = data.get('results', [])
        drugs   = []

        for item in results:
            openfda     = item.get('openfda', {})
            brand_names = openfda.get('brand_name', ['Unknown'])
            warnings    = item.get('warnings', ['No warnings listed'])
            purpose     = item.get('purpose', ['No purpose listed'])

            drugs.append({
                'brand_name': brand_names[0] if brand_names else 'Unknown',
                'warnings':   warnings[0][:300] if warnings else 'No warnings listed',
                'purpose':    purpose[0][:200]   if purpose  else 'No purpose listed',
            })

        return drugs

    except requests.exceptions.Timeout:
        return []
    except requests.exceptions.ConnectionError:
        return []
    except Exception:
        return []


def get_drug_interactions(drug_name: str) -> list:
    """
    Fetch drug interaction warnings from OpenFDA for a specific drug name.
    Returns a list of interaction strings.
    """
    try:
        response = requests.get(
            f"{OPENFDA_BASE_URL}/label.json",
            params={
                'search': f'openfda.brand_name:"{drug_name}"',
                'limit':  1,
            },
            timeout=5
        )

        if response.status_code != 200:
            return []

        data    = response.json()
        results = data.get('results', [])

        if not results:
            return []

        item         = results[0]
        interactions = item.get('drug_interactions', [])
        return [i[:300] for i in interactions[:3]]

    except Exception:
        return []


def search_drugs_by_symptom(symptom_name: str) -> list:
    """
    Search OpenFDA for drugs commonly associated with treating a symptom.
    Returns a list of drug dicts.
    """
    try:
        response = requests.get(
            f"{OPENFDA_BASE_URL}/label.json",
            params={
                'search': f'indications_and_usage:"{symptom_name}"',
                'limit':  3,
            },
            timeout=5
        )

        if response.status_code != 200:
            return []

        data    = response.json()
        results = data.get('results', [])
        drugs   = []

        for item in results:
            openfda     = item.get('openfda', {})
            brand_names = openfda.get('brand_name', [])
            generic     = openfda.get('generic_name', [])

            if brand_names or generic:
                drugs.append({
                    'brand_name':   brand_names[0] if brand_names else 'Unknown',
                    'generic_name': generic[0]     if generic     else 'Unknown',
                })

        return drugs

    except Exception:
        return []