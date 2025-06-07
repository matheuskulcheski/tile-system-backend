
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuração do CORS (permitindo requisições do frontend Vercel)
    CORS(app, resources={r"/*": {"origins": "https://tile-system-frontend-bbrg.vercel.app"}})

    # Configurações do app (exemplo)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Importar e registrar blueprints ou rotas aqui, ex:
    # from .routes.auth import auth_bp
    # app.register_blueprint(auth_bp)

    return app
