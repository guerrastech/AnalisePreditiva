from flask import Blueprint, render_template, request, redirect, send_file
import numpy as np
import pickle
from collections import Counter
from app.conexaoBD import connect_database
from app.utils import resultado_ocupacao, traduzir_genero, exportar_relatorio_pdf
from werkzeug.security import check_password_hash, generate_password_hash
from app.analises import (
    preparar_dados, analise_renda_total, analise_genero_renda,
    analise_ocupacao, analise_faixa_etaria, analise_escolaridade
)



main = Blueprint('main', __name__)

client = connect_database()
db = client['modeloPreditivo']
collection = db['previsoes']

model = pickle.load(open('modelo_preditivo.pkl', 'rb'))



@main.route("/home")
def home():
    return render_template("home.html")



@main.route("/NovaConsulta", methods=["GET", "POST"])
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


@main.route("/dashboard")
def dashboard():
    dados = list(collection.find({}, {"_id": 0}))
    dados = preparar_dados(dados)

    percentual_0, percentual_1 = analise_renda_total(dados)
    percentual_homens_mais_50k, percentual_mulheres_mais_50k = analise_genero_renda(dados)
    labels_ocupacao, percentuais_ocupacao = analise_ocupacao(dados)
    labels_faixa_etaria, valores_faixa_etaria = analise_faixa_etaria(dados)
    labels_escolaridade, percentuais_escolaridade = analise_escolaridade(dados)

    return render_template("dashboard.html", 
                           percentual_0=percentual_0,
                           percentual_1=percentual_1,
                           percentual_homens_mais_50k=percentual_homens_mais_50k,
                           percentual_mulheres_mais_50k=percentual_mulheres_mais_50k,
                           labels_ocupacao=labels_ocupacao,
                           percentuais_ocupacao=percentuais_ocupacao,
                           labels_faixa_etaria=labels_faixa_etaria,
                           valores_faixa_etaria=valores_faixa_etaria,
                           labels_escolaridade=labels_escolaridade,
                           percentuais_escolaridade=percentuais_escolaridade,
                           dados=dados)


@main.route("/exportar-relatorio")
def exportar_relatorio():
    dados = list(collection.find({}, {"_id": 0}))

    # Cálculos de estatísticas
    estatisticas = {
        "Distribuição Geral das Classes": [
            f"> 50K: {sum(d['previsao'] == '> 50K' for d in dados)}",
            f"<= 50K: {sum(d['previsao'] == '<= 50K' for d in dados)}"
        ],
        "Faixa Etária vs Classe Preditiva": [],
        "Escolaridade vs Classe Preditiva": [],
        "Top 5 Ocupações com Maior Renda > 50K": []
    }

    # Faixa etária
    faixas = [(18, 25), (26, 35), (36, 45), (46, 60), (61, 100)]
    for faixa in faixas:
        faixa_dados = [d for d in dados if faixa[0] <= d["idade"] <= faixa[1]]
        if faixa_dados:
            pct = sum(d["previsao"] == "> 50K" for d in faixa_dados) / len(faixa_dados) * 100
            estatisticas["Faixa Etária vs Classe Preditiva"].append(f"{faixa[0]}–{faixa[1]} anos: {pct:.2f}% > 50K")

    # Escolaridade
    escolaridades = {}
    for d in dados:
        esc = d["educacao"]
        if esc not in escolaridades:
            escolaridades[esc] = []
        escolaridades[esc].append(d["previsao"])
    
    for esc, previsoes in escolaridades.items():
        pct = previsoes.count("> 50K") / len(previsoes) * 100
        estatisticas["Escolaridade vs Classe Preditiva"].append(f"Educação {esc}: {pct:.2f}% > 50K")

    # Ocupações
    ocupacoes = {}
    for d in dados:
        d["ocupacao"] = resultado_ocupacao(d["ocupacao"])
        ocup = d["ocupacao"]
        if ocup not in ocupacoes:
            ocupacoes[ocup] = []
        ocupacoes[ocup].append(d["previsao"])
    
    top_ocup = sorted(ocupacoes.items(), key=lambda x: x[1].count("> 50K") / len(x[1]), reverse=True)[:5]
    for ocup, previsoes in top_ocup:
        pct = previsoes.count("> 50K") / len(previsoes) * 100
        estatisticas["Top 5 Ocupações com Maior Renda > 50K"].append(f"{ocup}: {pct:.2f}%")

    path = "relatorio_previsoes.pdf"
    exportar_relatorio_pdf(path, estatisticas)
    return send_file(path, as_attachment=True)


@main.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # Verifica se todos os campos foram preenchidos
        if not nome or not email or not senha:
            erro = "Todos os campos são obrigatórios"
        else:
            # Cria um hash da senha antes de salvar no banco
            senha_hash = generate_password_hash(senha)

            # Salva o usuário no MongoDB
            db['usuarios'].insert_one({
                "nome": nome,
                "email": email,
                "senha": senha_hash  # Armazena a senha de forma segura
            })
            return redirect("/login")

    return render_template("cadastro.html", erro=erro)
    erro = None
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # Salvar os usuarios no MongoDB
        if not nome or not email or not senha:
            erro = "Todos os campos são obrigatórios"
        else:
            # Salva o usuário
            db['usuarios'].insert_one({
                "nome": nome,
                "email": email,
                "senha": senha  
            })
            return redirect("/login")

    return render_template("cadastro.html", erro=erro)


@main.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        # Aqui você deve usar db['usuarios'] para acessar a coleção de usuários
        usuario_db = db['usuarios'].find_one({"email": usuario})  # Ou "usuario" se o campo for usuário

        # Verificação de usuario
        if usuario_db:
            # Verifica se a senha fornecida é válida
            if check_password_hash(usuario_db["senha"], senha):
                return redirect("/dashboard")
            else:
                erro = "Usuário ou senha incorretos"
        else:
            erro = "Usuário ou senha incorretos"

    return render_template("login.html", erro=erro)

    erro = None
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        usuario_db = mongo.db.usuarios.find_one({"usuario": usuario})


        # Verificação de usuario
        if usuario_db:
            # Verifica se a senha fornecida é válida
            if check_password_hash(usuario_db["senha"], senha):
                return redirect("/dashboard")
            else:
                erro = "Usuário ou senha incorretos"
        else:
            erro = "Usuário ou senha incorretos"

    return render_template("login.html", erro=erro)

