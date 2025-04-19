def resultado_ocupacao(numero_correspondente):
    match numero_correspondente:
        case 1: return "Administrativo e de escritório"
        case 2: return "Executivo e gerencial"
        case 3: return "Manipuladores e limpadores"
        case 4: return "Profissional especializado"
        case 5: return "Outros serviços"
        case 6: return "Vendas"
        case 7: return "Artesanato e reparos"
        case 8: return "Transporte e movimentação"
        case 9: return "Agricultura e pesca"
        case 10: return "Operador de máquina e inspeção"
        case 11: return "Suporte técnico"
        case 12: return "Desconhecido"
        case 13: return "Serviços de proteção"
        case 14: return "Forças armadas"
        case 15: return "Serviços domésticos privados"


def traduzir_genero(valor):
    return "Masculino" if valor == 1 else "Feminino"
