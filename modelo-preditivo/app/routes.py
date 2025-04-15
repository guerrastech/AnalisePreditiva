from flask import Blueprint, render_template, request, redirect
import numpy as np
import pickle
from collections import Counter
from app.conexaoBD import connect_database
from app.utils import resultado_ocupacao, traduzir_genero
from werkzeug.security import check_password_hash, generate_password_hash


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

    for d in dados:
        d["ocupacao"] = resultado_ocupacao(d["ocupacao"])
        d["genero"] = traduzir_genero(d["genero"])

    total = len(dados)
    contagem = Counter([d["previsao"] for d in dados])
    
    percentual_0 = (contagem.get("<= 50K", 0) / total) * 100 if total else 0
    percentual_1 = (contagem.get("> 50K", 0) / total) * 100 if total else 0




    ocupacoes = list(set(d["ocupacao"] for d in dados))  # pega nomes únicos já traduzidos
    ocupacoes.sort()  

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

