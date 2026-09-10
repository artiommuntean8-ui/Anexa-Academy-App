import sys
import os

# Adăugăm calea către directorul 'backend' în sys.path pentru a putea importa modulele app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.db.session import engine, SessionLocal, Base
from app.models.student import Student
from app.models.assignment import Assignment
from app.models.test_case import TestCase
from app.models.grade import Grade
from app.core.security import get_password_hash

def seed_db():
    print("🧹 Resetare și populare baza de date...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Creare Utilizatori
        users = [
            {"email": "profesor@anexa.md", "name": "Mihail Potlog", "role": "instructor", "code": "INST-001"},
            {"email": "artiom@anexa.md", "name": "Artiom Muntean", "role": "student", "code": "STUD-001"},
            {"email": "elev@anexa.md", "name": "Ion Popescu", "role": "student", "code": "STUD-002"}
        ]
        
        for u in users:
            student = Student(
                email=u["email"],
                full_name=u["name"],
                role=u["role"],
                student_code=u["code"],
                hashed_password=get_password_hash("student123" if u["role"] == "student" else "profesor123"),
                is_active=True
            )
            db.add(student)
        db.commit()

        # 2. Creare Exerciții
        assignments = [
            ("Print Salut", "Afișează mesajul: 'Salut, Anexa Academy!'", "print('Salut, Anexa Academy!')"),
            ("Suma a două numere", "Citește două numere și afișează suma.", "a = int(input())\nb = int(input())\nprint(a+b)"),
            ("Par sau Impar", "Afișează 'Par' sau 'Impar'.", "n = int(input())\nprint('Par' if n % 2 == 0 else 'Impar')"),
            ("Inversare Text", "Inversează textul dat.", "t = input()\nprint(t[::-1])"),
            ("Calcul Factorial", "Calculează factorialul unui număr.", "import math\nn = int(input())\nprint(math.factorial(n))")
        ]

        test_cases_data = [
            [("n/a", "Salut, Anexa Academy!", False)], # Ex 1
            [("3\n5", "8", False), ("-2\n10", "8", True), ("0\n0", "0", True)], # Ex 2
            [("4", "Par", False), ("7", "Impar", False), ("0", "Par", True)], # Ex 3
            [("python", "nohtyp", False), ("Anexa", "axenA", True)], # Ex 4
            [("5", "120", False), ("3", "6", True)] # Ex 5
        ]

        for i, (title, desc, code) in enumerate(assignments):
            assign = Assignment(title=title, description=desc, starter_code=code, course_id=1)
            db.add(assign)
            db.commit()
            db.refresh(assign)
            
            for tc in test_cases_data[i]:
                db.add(TestCase(assignment_id=assign.id, input_data=tc[0], expected_output=tc[1], is_hidden=tc[2]))
        
        db.commit()
        print("[SUCCESS] Baza de date a fost populată cu succes!")
        print("Credențiale:")
        print("Instructor: profesor@anexa.md / profesor123")
        print("Elev: artiom@anexa.md / student123")
        print("Elev: elev@anexa.md / student123")

    except Exception as e:
        print(f"[ERROR] {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
