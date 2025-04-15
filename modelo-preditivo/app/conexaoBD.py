from pymongo import MongoClient

def connect_database():
    uri = 'mongodb+srv://gabrielguerra190803:projetoapi@dados.tgjkrfh.mongodb.net/'  

    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("Conectado ao banco de dados")
        return client
    except Exception as error:
        print("Erro ao conectar ao banco de dados:", error)
        return None