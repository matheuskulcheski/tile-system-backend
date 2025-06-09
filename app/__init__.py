
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy import text

# Inicializa as extensões
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name=None):
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)

    # Configuração simplificada
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'production')

    # Configurações básicas
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'tile-system-secret-key-2024'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-2024'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Token não expira para simplificar

    # Configuração do banco de dados
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Para PostgreSQL no Render
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # SQLite local para desenvolvimento
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tile_system.db'

    # Configurações de timeout para evitar problemas
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_timeout': 20,
        'pool_recycle': 300,
        'pool_pre_ping': True
    }

    # Inicializa as extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Configura CORS de forma mais permissiva
    CORS(app, 
         resources={r"/*": {"origins": "*"}},
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

    # Registra os blueprints
    from .resources.auth_fixed import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Rota de verificação de saúde
    @app.route('/api/health')
    def health_check():
        return {"status": "ok", "message": "API is running"}, 200

    # Rota de teste de banco de dados
    @app.route('/api/db-test')
    def db_test():
        try:
            # Testa a conexão com o banco usando SQLAlchemy 2.x
            with db.engine.connect() as conn:
                conn.execute(text('SELECT 1'))
            return {"status": "ok", "message": "Database connection working"}, 200
        except Exception as e:
            return {"status": "error", "message": f"Database error: {str(e)}"}, 500

    return app
