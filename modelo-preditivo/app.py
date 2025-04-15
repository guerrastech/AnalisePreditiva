from flask import Flask, render_template, request
import pickle
import numpy as np
from conexaoBD import connect_database
from collections import Counter

# Conectar ao MongoDB
client = connect_database()
db = client['modeloPreditivo']
collection = db['previsoes']

# Iniciar o app Flask
app = Flask(__name__)

# Carregar o modelo preditivo
model = pickle.load(open('modelo_preditivo.pkl', 'rb'))


# 🔍 Função auxiliar para traduzir o código de ocupação
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

# 🔍 Função auxiliar para traduzir o código de genero
def traduzir_genero(valor):
    return "Masculino" if valor == 1 else "Feminino"

@app.route("/NovaConsulta", methods=["GET", "POST"])
def index():
    previsao = None

    if request.method == "POST":
        # Captura os dados do formulário
        idade = int(request.form.get("age"))
        genero = int(request.form.get("sex"))
        ocupacao = int(request.form.get("occupation"))
        educacao = int(request.form.get("education-num"))
        capital = float(request.form.get("capital-gain"))

        # Dados para o modelo
        features = np.array([[educacao, idade, ocupacao, genero, capital]])  # ordem conforme o treino
        previsao = model.predict(features)[0]  # pega só o valor da previsão
        if previsao == 0:
            previsao = "<= 50K"
        else:
            previsao = "> 50K"

        # Salvar no MongoDB
        collection.insert_one({
            "idade": idade,
            "genero": genero,
            "ocupacao": ocupacao,
            "educacao": educacao,
            "capital_gain": capital,
            "previsao": str(previsao)
        })

        # Retornar a página com a previsão
        return render_template("index.html", previsao=previsao)

    return render_template("index.html", previsao=None)


@app.route("/dashboard")
def dashboard():
    dados = list(collection.find({}, {"_id": 0}))

    for d in dados:
        d["ocupacao"] = resultado_ocupacao(d["ocupacao"])
        d["genero"] = traduzir_genero(d["genero"])

    total = len(dados)
    contagem = Counter([d["previsao"] for d in dados])
    
    percentual_0 = (contagem.get("<= 50K", 0) / total) * 100 if total else 0
    percentual_1 = (contagem.get("> 50K", 0) / total) * 100 if total else 0




    ocupacoes = list(set(d["ocupacao"] for d in dados))  # pega nomes únicos já traduzidos
    ocupacoes.sort()  # só pra manter ordem alfabética

    labels_ocupacao = []
    percentuais_ocupacao = []

    for ocup in ocupacoes:
        pessoas_na_ocup = [d for d in dados if d["ocupacao"] == ocup]
        total_ocup = len(pessoas_na_ocup)
        com_mais_50k = sum(1 for d in pessoas_na_ocup if d["previsao"] == "> 50K")
        
        percentual = (com_mais_50k / total_ocup) * 100 if total_ocup else 0
        labels_ocupacao.append(ocup)
        percentuais_ocupacao.append(round(percentual, 2))



    homens = [d for d in dados if d["genero"] == "Masculino"]
    mulheres = [d for d in dados if d["genero"] == "Feminino"]

    homens_mais_50k = sum(1 for d in homens if d["previsao"] == "> 50K")
    mulheres_mais_50k = sum(1 for d in mulheres if d["previsao"] == "> 50K")

    percentual_homens_mais_50k = (homens_mais_50k / len(homens)) * 100 if homens else 0
    percentual_mulheres_mais_50k = (mulheres_mais_50k / len(mulheres)) * 100 if mulheres else 0

    return render_template("dashboard.html", 
                           percentual_0=percentual_0, 
                           percentual_1=percentual_1,
                           percentual_homens_mais_50k=percentual_homens_mais_50k,
                           percentual_mulheres_mais_50k=percentual_mulheres_mais_50k,
                           labels_ocupacao=labels_ocupacao,
                           percentuais_ocupacao=percentuais_ocupacao,
                           dados=dados)





if __name__ == "__main__":
    app.run(debug=True)
