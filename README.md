# MedAssist - Symptom Checker & First Aid Guide

[Flask] [Python 3.9] [SQLite] [Bootstrap 5] [OpenFDA API]

**A comprehensive healthcare web application for symptom assessment and first aid guidance**

---

## Disclaimer

> **IMPORTANT:** This application is for educational and informational purposes only. It does not constitute medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional. If you are experiencing a medical emergency, call 999 or 112 immediately.

---

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Severity System](#severity-system)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Setup Instructions](#setup-instructions)
- [Testing](#testing)
- [API Integration](#api-integration)
- [Deployment](#deployment)
- [Development History](#development-history)

---

## Features

| Category | Features |
|----------|----------|
| Symptom Checker | Multi-step questionnaire with session management |
| | Rule-based scoring engine matching symptoms to conditions |
| | Severity rating (Low, Moderate, Urgent, Emergency) |
| Drug Information | Live drug warnings via OpenFDA API |
| | Drug interaction checker |
| First Aid | Comprehensive guide library with step-by-step instructions |
| | Print functionality for guides |
| User System | Registration, login, logout |
| | Symptom history dashboard |
| | Personal profile page |
| Tools | BMI calculator with health categories |
| UI/UX | Severity color coding across all pages |
| | Responsive Bootstrap 5 design |
| | Medical disclaimer on every page |
| Emergency | Emergency contacts page with Kenya hotlines |
| Error Handling | Custom 404 error page |
| Development | Jupyter Notebooks for data analysis |
| | Unit and integration tests |

---

## Technology Stack

**Environment & Backend**
- Anaconda / Python 3.9
- Flask 3.0.3 (Application framework)
- Flask-Login (Authentication)
- Flask-Bcrypt (Password hashing)
- Flask-SQLAlchemy (ORM)

**Database**
- SQLite (Development)
- SQLAlchemy (Database abstraction)

**Frontend**
- Bootstrap 5 (Responsive framework)
- Font Awesome 6 (Icons)
- Jinja2 (Templating)
- Custom CSS/JS

**APIs & External Services**
- OpenFDA Drug Label API

**Development & Testing**
- Jupyter Notebook (Analysis)
- pandas, matplotlib (Data visualization)
- pytest, pytest-flask (Testing)
- Git (Version control)

---

## Severity System

| Level | Color | Meaning | Action Required |
|-------|-------|---------|-----------------|
| Low | Green | Minor, self-treatable condition | Home care |
| Moderate | Amber | Monitor symptoms | See doctor if no improvement |
| Urgent | Orange | Medical attention needed | Seek care today |
| Emergency | Red | Critical situation | Call emergency services immediately |

---


---

## Database Schema

| Table | Description |
|-------|-------------|
| `user` | Registered users with hashed passwords |
| `symptom_history` | Saved symptom check results per user |
| `symptom` | Individual symptoms with slugs and body areas |
| `condition` | Medical conditions with severity levels |
| `symptom_condition` | Many-to-many junction table |
| `question` | Questionnaire questions with JSON options |
| `firstaid_guide` | Step-by-step first aid guides |
| `user_session` | Session tokens for anonymous tracking |

---

## Setup Instructions

### Prerequisites
- Anaconda or Miniconda installed
- Git installed

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd med-assist
```
