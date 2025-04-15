def resultado_ocupacao(numero_correspondente):
    match numero_correspondente:
        case 1: return "Adm-clerical"
        case 2: return "Exec-managerial"
        case 3: return "Handlers-cleaners"
        case 4: return "Prof-specialty"
        case 5: return "Other-service"
        case 6: return "Sales"
        case 7: return "Craft-repair"
        case 8: return "Transport-moving"
        case 9: return "Farming-fishing"
        case 10: return "Machine-op-inspct"
        case 11: return "Tech-support"
        case 12: return "?"
        case 13: return "Protective-serv"
        case 14: return "Armed-Forces"
        case 15: return "Priv-house-serv"


def traduzir_genero(valor):
    return "Masculino" if valor == 1 else "Feminino"
