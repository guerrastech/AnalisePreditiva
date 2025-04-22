from pymongo import MongoClient

def test_mongodb_connection():
    print("Iniciando o teste de conexão com o MongoDB...")

    try:
        client = MongoClient("mongodb+srv://gabrielguerra190803:projetoapi@dados.tgjkrfh.mongodb.net/")
        db = client["nome_do_banco"]
        collections = db.list_collection_names()
        print(f"Coleções no banco: {collections}")
        assert isinstance(collections, list)
        print("✅ Conexão com MongoDB bem-sucedida.")
    except Exception as e:
        print(f"❌ Erro ao conectar com o MongoDB: {e}")
        assert False, f"Erro ao conectar com o MongoDB: {e}"


if __name__ == "__main__":
    test_mongodb_connection()
