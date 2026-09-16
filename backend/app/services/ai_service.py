async def get_socratic_hint(student_code: str, error_log: str, hint_count: int) -> str:
    # Simulare raspuns AI pentru MVP
    hints = [
        'Ai incercat sa verifici daca parantezele sunt toate inchise? ??',
        'Se pare ca variabila folosita nu a fost definita. Uita-te la linia de mai sus! ??',
        'Indiciu: Python este foarte atent la spa?ii. Verifica indentarea la linia 3! ??'
    ]
    return hints[min(hint_count, len(hints) - 1)]
