import sys
import os
import pickle

# Adiciona o diretório principal ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Carregar o modelo
model_path = os.path.join(os.path.dirname(__file__), '..', 'modelo_preditivo.pkl')
model = pickle.load(open(os.path.abspath(model_path), 'rb'))

# Importa a função create_app de __init__.py
from app import create_app

# Cria a instância do app Flask
app = create_app()

def test_home_route():
    client = app.test_client()
    response = client.get('/home')  # Ou a rota que você deseja testar
    
    print(f"Resposta da rota '/home': {response.status_code}")  # Exibe o código de status da resposta
    assert response.status_code == 200, f"Erro: código de status esperado 200, mas obteve {response.status_code}"  # Mensagem de erro se falhar
    
    print("Teste da rota '/home' passou com sucesso!")  # Mensagem de sucesso

if __name__ == "__main__":
    test_home_route()