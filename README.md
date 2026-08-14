# Academy Student Dashboard

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![PySide6](https://img.shields.io/badge/PySide6-Qt6-41CD52?style=for-the-badge&logo=qt)](https://www.qt.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://www.python.org)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org)
[![JWT](https://img.shields.io/badge/JWT-Auth-black?style=for-the-badge&logo=jsonwebtokens)](https://jwt.io)

**Academy Student Dashboard** este o platformă completă dedicată studenților și profesorilor din cadrul **Academiei ArkiTech**. Proiectul integrează o aplicație desktop performantă dezvoltată în **PySide6 (Qt6)** cu un backend asincron securizat dezvoltat în **FastAPI**.

---

## 👨‍💻 Autor & Drepturi de Autor

- **Autor:** Artiom Muntean
- **Organizație:** [Academia ArkiTech](https://arkitech.academy)
- **Rol:** Arhitect & Lead Software Engineer

---

## 🏛️ Arhitectura Sistemului

Sistemul funcționează pe o arhitectură decuplată **Desktop Client — REST API (JWT)**:

```text
┌────────────────────────────────────────────────────────┐
│             Desktop Student Dashboard (Client)         │
│                 (PySide6 / Qt6 Native GUI)             │
│   ├── LoginView (Autentificare JWT)                    │
│   ├── DashboardView (Statistici KPI & Carduri Cursuri) │
│   ├── CoursesView (Catalog Cursuri & Înscrieri)        │
│   ├── AssignmentsView (Teme & Termene Limită)          │
│   ├── GradesView (Note & Feedback Profesori)           │
│   └── ProfileView (Date Student & Securitate)          │
└───────────────────────────┬────────────────────────────┘
                            │
              HTTP / JSON + Bearer JWT Token
                            │
┌───────────────────────────▼────────────────────────────┐
│                    FastAPI Backend                     │
│   ├── Autentificare & Criptare Bcrypt + JWT (HS256)    │
│   ├── Routing & Validare (Pydantic v2)                 │
│   ├── Securitate & CORS Middleware                     │
│   └── ORM & Gestiune Tranzacții (SQLAlchemy)           │
└───────────────────────────┬────────────────────────────┘
                            │
             SQLite (Default) / PostgreSQL
                            │
┌───────────────────────────▼────────────────────────────┐
│             Relational Database Engine                 │
└────────────────────────────────────────────────────────┘
```

---

## 📁 Structura Proiectului

```text
Anexa App/
├── backend/                        # Backend REST API (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # Punctul principal de intrare FastAPI, Lifespan & CORS
│   │   ├── core/                   # Configurări globale, securitate și setări
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # Pydantic Settings
│   │   │   └── security.py         # Bcrypt Password Hashing & JWT Utilities
│   │   ├── api/                    # Rute și endpoint-uri REST API
│   │   │   ├── __init__.py
│   │   │   ├── deps.py             # Dependențe JWT (get_current_user)
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── api.py          # Agregator de routere v1
│   │   │       └── endpoints/
│   │   │           ├── __init__.py
│   │   │           ├── auth.py     # Autentificare (Login, Register, Me)
│   │   │           ├── students.py # CRUD Studenți & Dashboard Aggregator
│   │   │           ├── courses.py  # Catalog cursuri & înscrieri
│   │   │           ├── assignments.py # Gestiune teme
│   │   │           ├── grades.py   # Note și evaluări
│   │   │           └── health.py   # Endpoint status
│   │   ├── models/                 # Modele SQLAlchemy ORM
│   │   │   ├── __init__.py
│   │   │   ├── student.py
│   │   │   ├── course.py
│   │   │   ├── enrollment.py
│   │   │   ├── assignment.py
│   │   │   └── grade.py
│   │   ├── schemas/                # Scheme Pydantic DTO (Request/Response)
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── student.py
│   │   │   ├── course.py
│   │   │   ├── enrollment.py
│   │   │   ├── assignment.py
│   │   │   ├── grade.py
│   │   │   └── dashboard.py
│   │   └── db/                     # Sesiune DB și inițializare date demo
│   │       ├── __init__.py
│   │       ├── session.py
│   │       └── init_db.py
│   ├── .env.example
│   ├── .gitignore
│   └── requirements.txt
│
├── client/                         # Aplicație Desktop Client (PySide6)
│   ├── src/
│   │   ├── __init__.py
│   │   ├── config.py               # Configurare client & URL API
│   │   ├── components/             # Componente UI refolosibile
│   │   │   ├── __init__.py
│   │   │   ├── header.py           # Header cu status server și titlu
│   │   │   ├── sidebar.py          # Meniu lateral și badge profil
│   │   │   └── stat_card.py        # Carduri KPI
│   │   ├── styles/
│   │   │   ├── __init__.py
│   │   │   └── theme.py            # Foaie de stil QSS Dark Theme
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── api_client.py       # Client HTTP requests cu Bearer Token
│   │   │   └── auth_service.py     # Gestiune sesiune utilizator
│   │   ├── views/                  # Ecranele aplicației desktop
│   │   │   ├── __init__.py
│   │   │   ├── login_view.py       # Autentificare
│   │   │   ├── dashboard_view.py   # Panou principal
│   │   │   ├── courses_view.py     # Cursuri
│   │   │   ├── assignments_view.py # Teme
│   │   │   ├── grades_view.py      # Note
│   │   │   └── profile_view.py     # Profil
│   │   └── main.py                 # Punct de intrare Desktop GUI
│   ├── .gitignore
│   ├── README.md
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## 🚀 Ghid de Pornire Rapidă

### 1. Pornire Server Backend
Într-un terminal:
```powershell
cd backend
python -m uvicorn app.main:app --reload
```
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 2. Pornire Desktop Client
Într-un al doilea terminal (din rădăcina proiectului):
```powershell
python client/src/main.py
```

### 🔑 Credențiale Demo:
- **Email:** `artiom.muntean@arkitech.academy`
- **Parolă:** `ArkiTech2026!`
