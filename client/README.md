# Academy Student Dashboard — Desktop Client (PySide6 / Qt6)

Aplicația Desktop Client oferă o interfață grafică modernă, asincronă și intuitivă pentru studenții din cadrul **Academiei ArkiTech**, dezvoltată în **PySide6 (Qt6)**.

---

## ✨ Funcționalități Principale

- 🔐 **Autentificare Securizată JWT:** Ecran de conectare integrat cu backend-ul FastAPI, memorare sesiune și gestionare securizată a token-urilor Bearer.
- 📊 **Panou Principal (Dashboard):** Carduri KPI (număr cursuri, credite totale ECTS, medie generală GPA, teme active), lista cursurilor înscrise, teme viitoare și ultimele note primite.
- 📚 **Catalog Cursuri:** Vizualizare completă a cursurilor universitare și posibilitatea de înscriere instantanee.
- 📝 **Teme & Proiecte:** Tabel detaliat cu temele de laborator, punctaj maxim și termene limită.
- 🎯 **Note & Situație Academică:** Istoric complet al notelor și feedback-ul detaliat primit de la instructori.
- 👤 **Profil Student & Securitate:** Vizualizarea datelor de identificare (cod student, departament, semestru) și formular pentru actualizarea parolei.

---

## 🏗️ Structura Modulului Client

```text
client/
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── header.py          # Bară superioară cu titlu, stare server și refresh
│   │   ├── sidebar.py         # Meniu lateral de navigare și badge utilizator
│   │   └── stat_card.py       # Carduri statistice pentru KPI-uri
│   ├── styles/
│   │   ├── __init__.py
│   │   └── theme.py           # Foaie de stil QSS temă Dark modernă
│   ├── services/
│   │   ├── __init__.py
│   │   ├── api_client.py      # Client HTTP (Requests) cu suport JWT Token
│   │   └── auth_service.py    # Gestiunea sesiunii de autentificare și profil
│   ├── views/
│   │   ├── __init__.py
│   │   ├── login_view.py      # Ecran de autentificare
│   │   ├── dashboard_view.py  # Panou principal agregat
│   │   ├── courses_view.py    # Catalog și înscrieri cursuri
│   │   ├── assignments_view.py# Teme și proiecte
│   │   ├── grades_view.py     # Note și progres
│   │   └── profile_view.py    # Profil student și schimbare parolă
│   ├── config.py              # Configurări client (URL API, Timeout)
│   └── main.py                # Punctul principal de intrare (QApplication)
├── requirements.txt           # Dependențe (PySide6, requests)
└── README.md
```

---

## 🚀 Ghid de Pornire

### 1. Asigurați-vă că Backend-ul este pornit
Într-un terminal separat:
```powershell
cd backend
uvicorn app.main:app --reload
```

### 2. Porniți Aplicația Desktop
Din rădăcina proiectului:
```powershell
python client/src/main.py
```

### 🔑 Credențiale Demo Pre-configurate:
- **Email:** `artiom.muntean@arkitech.academy`
- **Parolă:** `ArkiTech2026!`
