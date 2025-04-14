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


# 🔍 Função auxiliar para traduzir o código de ocupação (se quiser usar em alguma exibição)
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
    # Pega todos os dados salvos no MongoDB
    dados = list(collection.find({}, {"_id": 0}))

    # Conta quantas predições de cada tipo
    total = len(dados)
    contagem = Counter([d["previsao"] for d in dados])
    
    percentual_0 = (contagem.get("<= 50K", 0) / total) * 100 if total else 0
    percentual_1 = (contagem.get("> 50K", 0) / total) * 100 if total else 0

    return render_template("dashboard.html", 
                           percentual_0=percentual_0, 
                           percentual_1=percentual_1,
                           dados=dados)



if __name__ == "__main__":
    app.run(debug=True)
