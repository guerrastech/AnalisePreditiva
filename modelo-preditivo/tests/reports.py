def generate_report(data):
    if not data:
        raise ValueError("Dados vazios")
    return {"total": len(data), "valido": True}
