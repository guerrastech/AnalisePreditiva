from collections import Counter
from app.utils import resultado_ocupacao, traduzir_genero

def preparar_dados(dados):
    for d in dados:
        d["ocupacao"] = resultado_ocupacao(d["ocupacao"])
        d["genero"] = traduzir_genero(d["genero"])
    return dados

def analise_renda_total(dados):
    total = len(dados)
    contagem = Counter([d["previsao"] for d in dados])
    percentual_0 = (contagem.get("<= 50K", 0) / total) * 100 if total else 0
    percentual_1 = (contagem.get("> 50K", 0) / total) * 100 if total else 0
    return percentual_0, percentual_1

def analise_genero_renda(dados):
    homens = [d for d in dados if d["genero"] == "Masculino"]
    mulheres = [d for d in dados if d["genero"] == "Feminino"]
    homens_mais_50k = sum(1 for d in homens if d["previsao"] == "> 50K")
    mulheres_mais_50k = sum(1 for d in mulheres if d["previsao"] == "> 50K")
    percentual_homens = (homens_mais_50k / len(homens)) * 100 if homens else 0
    percentual_mulheres = (mulheres_mais_50k / len(mulheres)) * 100 if mulheres else 0
    return percentual_homens, percentual_mulheres

def analise_ocupacao(dados):
    ocupacoes = sorted(set(d["ocupacao"] for d in dados))
    labels = []
    percentuais = []
    for ocup in ocupacoes:
        pessoas = [d for d in dados if d["ocupacao"] == ocup]
        total = len(pessoas)
        mais_50k = sum(1 for d in pessoas if d["previsao"] == "> 50K")
        percentual = (mais_50k / total) * 100 if total else 0
        labels.append(ocup)
        percentuais.append(round(percentual, 2))
    return labels, percentuais

def analise_faixa_etaria(dados):
    faixas = {'18-25': 0, '26-35': 0, '36-45': 0, '46-60': 0, '60+': 0}
    for d in dados:
        idade = d["idade"]
        if idade <= 25:
            faixa = '18-25'
        elif idade <= 35:
            faixa = '26-35'
        elif idade <= 45:
            faixa = '36-45'
        elif idade <= 60:
            faixa = '46-60'
        else:
            faixa = '60+'
        if d["previsao"] == "> 50K":
            faixas[faixa] += 1
    return list(faixas.keys()), list(faixas.values())

def analise_escolaridade(dados):
    escolaridade_dict = {}
    for d in dados:
        esc = d["educacao"]
        if esc not in escolaridade_dict:
            escolaridade_dict[esc] = {"total": 0, ">50K": 0}
        escolaridade_dict[esc]["total"] += 1
        if d["previsao"] == "> 50K":
            escolaridade_dict[esc][">50K"] += 1
    labels = sorted(escolaridade_dict.keys())
    percentuais = [
        round((escolaridade_dict[e][">50K"] / escolaridade_dict[e]["total"]) * 100, 2)
        for e in labels
    ]
    return labels, percentuais
