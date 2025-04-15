from flask import Flask

def create_app():
    import os
    app = Flask(__name__, template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates")))
    app.secret_key = 'projetoAPI'  # Defina uma chave segura depois

    from .routes import main
    app.register_blueprint(main)

    return app
