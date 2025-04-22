from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

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


def exportar_relatorio_pdf(path, estatisticas):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Relatório de Previsões")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    y = height - 120

    for titulo, conteudo in estatisticas.items():
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, titulo)
        y -= 20

        c.setFont("Helvetica", 10)
        for linha in conteudo:
            c.drawString(70, y, linha)
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50

        y -= 10

    c.save()