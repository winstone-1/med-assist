# MedAssist – Symptom Checker & First Aid Guide

## Project Explanation
MedAssist is a Flask-based web application that helps users identify possible health conditions by answering a multi-step questionnaire about their symptoms. The app suggests matching conditions with severity indicators (Low → Medium → Emergency) and provides downloadable first aid guides for common injuries like burns, cuts, choking, and sprains. A prominent medical disclaimer emphasizes that this is an educational tool only, not a substitute for professional medical advice.

## UI Technology
- **Flask** – Python web framework handling routes, requests, and server-side logic
- **Jinja2 Templates** – HTML templating with template inheritance (`base.html` extended by all pages)
- **Bootstrap 5** – Responsive CSS framework for styling, modals, and navigation
- **JavaScript (vanilla)** – Form validation, dynamic severity color coding, and PDF trigger buttons

## Database
- **SQLite** with **SQLAlchemy ORM** – Lightweight, serverless database perfect for prototyping
- **Tables:**
  - `Question` – Stores multi-step symptom questions and options
  - `Condition` – Medical conditions with severity levels and recommendations
  - `Symptom` – Individual symptoms linked to conditions
  - `SymptomCondition` – Junction table linking symptoms to conditions with weight scores
  - `FirstAidGuide` – First aid content with title, steps, category, and emergency warnings

## Python Concepts Implemented

| Concept | How It's Used in MedAssist |
|---------|----------------------------|
| **Flask Routes & HTTP Methods** | `@app.route()` decorators with GET (display forms) and POST (process symptom answers, send messages) |
| **Jinja2 Templating** | Template inheritance (`{% extends "base.html" %}`), conditionals (`{% if severity == 'high' %}`), loops (`{% for condition in conditions %}`), and filters (`{{ timestamp|datetime }}`) |
| **SQLAlchemy ORM** | Defining database models as Python classes, establishing relationships (`db.relationship`), querying (`Condition.query.filter_by(severity='high').all()`) |
| **Session Management** | Storing symptom answers across the multi-step form using Flask's `session` dictionary (`session['answers'] = {'headache': True}`) |
| **Request/Response Handling** | Accessing form data via `request.form.get()` or JSON via `request.get_json()`, returning `render_template()` or `redirect()` or `jsonify()` |
| **Conditional Logic & Decision Tree** | Matching user symptoms to conditions using if/elif chains or weighted scoring algorithm (`if 'fever' in symptoms and 'cough' in symptoms: return 'Common Cold'`) |
| **Error Handling** | Try/except blocks for PDF generation failures, API call timeouts (if integrated), database connection errors, and file I/O operations |
| **File Handling & PDF Export** | Generating PDFs using WeasyPrint/ReportLab with `render_template()` for HTML-to-PDF conversion, saving to `/exports` folder, sending as downloadable response with `send_file()` |
| **Environment Variables** | Storing Flask `SECRET_KEY` and any API keys (Infermedica, Google Places, Twilio) in a `.env` file loaded via `python-dotenv` |
| **Functions & Modularity** | Creating reusable functions like `match_symptoms(symptoms_list)`, `generate_pdf(guide_id)`, `cache_api_response()`, and `send_sms_alert()` for clean, testable code |
| **Decorators** | Custom `@login_required` decorator (if user authentication added) and Flask's built-in `@app.before_request` for global actions like enforcing disclaimer acceptance |
| **List & Dictionary Comprehensions** | Efficiently filtering conditions: `[c for c in conditions if c.severity == 'high']` or building symptom option dicts from database queries |
| **JSON Parsing** | If integrating external APIs (Infermedica, OpenFDA), using `response.json()` to parse API responses and extract condition names, drug info, or hospital locations |

 
## 2. Project Folder Structure
 
```
medassist/
├── app.py                          # Main Flask application & factory
├── models.py                       # SQLAlchemy database models
├── symptom_matcher.py              # Decision tree / rule-based logic
├── seed.py                         # Populate DB with symptoms & first aid
├── environment.yml                 # Conda environment definition
├── requirements.txt                # Pip-compatible dependency list
├── .env                            # SECRET_KEY and config variables
│
├── notebook/
│   ├── decision_tree_test.ipynb    # Test & visualise symptom matching
│   ├── query_prototyping.ipynb     # Prototype SQLAlchemy queries
│   ├── data_analysis.ipynb         # Symptom pattern analysis
│   └── export_guides.ipynb         # Export first aid guides to CSV/PDF
│
├── templates/
│   ├── base.html                   # Base template: navbar, footer, disclaimer
│   ├── index.html                  # Landing page
│   ├── symptom_form.html           # Multi-step symptom questionnaire
│   ├── results.html                # Possible conditions + severity
│   ├── firstaid_list.html          # Browse all first aid guides
│   ├── firstaid_detail.html        # Guide detail + PDF export button
│   ├── emergency.html              # Emergency contacts & hotlines
│   └── disclaimer.html             # Full medical disclaimer page
│
├── static/
│   ├── css/
│   │   └── style.css               # Custom styling overrides
│   ├── js/
│   │   ├── form_validation.js      # Client-side step validation
│   │   └── severity_colors.js      # Dynamic severity colour coding
│   └── images/
│       └── icons/                  # Severity level SVG icons
│
├── instance/
│   └── medassist.db                # Auto-generated SQLite database
│
├── exports/
│   └── firstaid_pdfs/              # Generated PDF files
│
└── tests/
    ├── test_models.py              # Unit tests for DB models
    ├── test_matcher.py             # Unit tests for symptom matching
    └── test_routes.py              # Integration tests for Flask routes
```