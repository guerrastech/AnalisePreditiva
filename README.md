# 📊 Dashboard de Previsões com Flask e Machine Learning

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask)
![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?logo=mongodb)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-yellow)
![Licença](https://img.shields.io/badge/Licença-MIT-blue)

Este projeto é um sistema web desenvolvido com Flask que permite realizar previsões com base em dados enviados pelo usuário. Ele utiliza um modelo de Machine Learning (Random Forest) para classificar os dados e exibe os resultados por meio de um dashboard interativo com gráficos (barras). Os dados são armazenados em um banco de dados MongoDB.

---

## 🚀 Funcionalidades

- Cadastro e autenticação de usuários
- Previsões com base em um modelo treinado
- Armazenamento dos dados no MongoDB
- Visualização dos resultados no dashboard:
  - Gráfico de distribuição de classes (barras)
  - Tabela com dados armazenados

---

## 🧠 Tecnologias Utilizadas

- Python 3.x
- Flask
- MongoDB (via `pymongo`)
- Pandas
- Scikit-learn (RandomForest)
- HTML + CSS
- JavaScript (para interações com gráficos)
- Chart.js (gráficos no dashboard)

---

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/guerrastech/AnalisePreditiva.git
cd modelo-preditivo
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Instale as dependências:

```bash
pip install -r req.txt

```

4. Inicie o servidor Flask:

```bash

python run.py

```

5. Acesse o navegador:

http://127.0.0.1:5000/login


## ⚙️ Estrutura do Projeto

```
projeto-ia/
├── app/
│   ├── __init__.py              # Inicialização do módulo Flask
|   ├── analises.py              # Inicialização do módulo Flask
│   ├── conexaoBD.py             # Conexão com MongoDB
│   ├── modelo.py                # Carregamento e uso do modelo preditivo
│   ├── routes.py                # Rotas principais da aplicação
│   ├── utils.py                 # Funções auxiliares
│
├── static/
│   ├── css/                     # Arquivos CSS
│   └── js/                      # Scripts JavaScript
│
├── templates/
│   ├── cadastro.html            # Página de cadastro de usuários
│   ├── dashboard.html          # Dashboard com gráficos
│   ├── home.html                # Página principal
│   ├── index.html               # Página inicial/login
│   └── login.html               # Página de login
│
├── modelo_preditivo.pkl         # Modelo treinado (serializado com Pickle)
├── income_evaluation.csv        # Base de dados utilizada
├── run.py                       # Ponto de entrada principal da aplicação
├── req.txt                      # Lista de dependências (requirements.txt)
└── README.md                    # Documentação do projeto


```


## 🧪 Exemplo de Uso

1. Acesse a página inicial e faça uma nova consulta.
2. Preencha os dados solicitados (ex: idade, ocupação, gênero, etc).
3. O sistema faz a previsão com base no modelo treinado.
4. Os resultados são salvos no MongoDB e exibidos no Dashboard com gráficos.

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request


## 📜 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).


## 👥 Equipe

- [Gabriel Guerra](https://github.com/guerrastech) - Desenvolvedor Backend



