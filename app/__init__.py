import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .config import config

# Inicialização das extensões
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='default'):
    """Função factory para criar a aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializa as extensões com a aplicação
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Configuração adicional do JWT
    @jwt.user_identity_loader
    def user_identity_lookup(user_id):
        return str(user_id)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        from app.models.user import User
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()
    
    # Cria diretório de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'projects'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'temp'), exist_ok=True)
    
    # Registra os blueprints
    from .resources.auth import auth_bp
    from .resources.client import client_bp
    from .resources.project import project_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(client_bp, url_prefix='/api/clients')
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'message': 'API is running'}
    
    return app

