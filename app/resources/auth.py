from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.models import User
from app import db
import traceback

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint de login corrigido para evitar timeouts"""
    try:
        # Log da requisição recebida
        current_app.logger.info("Requisição de login recebida")
        
        # Obtém os dados do formulário
        data = request.get_json()
        
        if not data:
            current_app.logger.error("Nenhum dado JSON recebido")
            return jsonify({"error": "Nenhum dado recebido"}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        current_app.logger.info(f"Tentativa de login para email: {email}")
        
        if not email or not password:
            current_app.logger.error("Email ou senha não fornecidos")
            return jsonify({"error": "Email e senha são obrigatórios"}), 400
        
        # Busca o usuário pelo email com timeout
        try:
            user = User.query.filter_by(email=email).first()
            current_app.logger.info(f"Usuário encontrado: {user is not None}")
        except Exception as db_error:
            current_app.logger.error(f"Erro ao consultar banco de dados: {str(db_error)}")
            return jsonify({"error": "Erro interno do servidor"}), 500
        
        if not user:
            current_app.logger.warning(f"Usuário não encontrado para o email: {email}")
            return jsonify({"error": "Email ou senha inválidos"}), 401
        
        # Verifica a senha com timeout
        try:
            password_valid = check_password_hash(user.password, password)
            current_app.logger.info(f"Verificação de senha: {'válida' if password_valid else 'inválida'}")
        except Exception as pwd_error:
            current_app.logger.error(f"Erro ao verificar senha: {str(pwd_error)}")
            return jsonify({"error": "Erro interno do servidor"}), 500
        
        if not password_valid:
            current_app.logger.warning(f"Senha inválida para o usuário: {email}")
            return jsonify({"error": "Email ou senha inválidos"}), 401
        
        # Cria o token de acesso
        try:
            access_token = create_access_token(identity=str(user.id))
            current_app.logger.info(f"Token gerado para o usuário: {email}")
        except Exception as token_error:
            current_app.logger.error(f"Erro ao gerar token: {str(token_error)}")
            return jsonify({"error": "Erro interno do servidor"}), 500
        
        # Retorna o token e os dados do usuário
        response_data = {
            "message": "Login realizado com sucesso",
            "token": access_token,
            "user": {
                "id": user.id,
                "nome": user.nome,
                "email": user.email,
                "role": user.role
            }
        }
        
        current_app.logger.info(f"Login bem-sucedido para: {email}")
        return jsonify(response_data), 200
    
    except Exception as e:
        current_app.logger.error(f"Erro inesperado no login: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """Endpoint de registro de usuário"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Nenhum dado recebido"}), 400
        
        nome = data.get('nome', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        role = data.get('role', 'user')
        
        if not nome or not email or not password:
            return jsonify({"error": "Nome, email e senha são obrigatórios"}), 400
        
        # Verifica se o usuário já existe
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email já está em uso"}), 409
        
        # Cria o novo usuário
        from werkzeug.security import generate_password_hash
        new_user = User(
            nome=nome,
            email=email,
            password=generate_password_hash(password),
            role=role
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "message": "Usuário criado com sucesso",
            "user": {
                "id": new_user.id,
                "nome": new_user.nome,
                "email": new_user.email,
                "role": new_user.role
            }
        }), 201
    
    except Exception as e:
        current_app.logger.error(f"Erro no registro: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Erro interno do servidor"}), 500

@auth_bp.route('/test', methods=['GET'])
def test_auth():
    """Endpoint de teste para verificar se a autenticação está funcionando"""
    try:
        # Conta o número de usuários
        user_count = User.query.count()
        
        return jsonify({
            "message": "Autenticação funcionando",
            "user_count": user_count,
            "status": "ok"
        }), 200
    
    except Exception as e:
        current_app.logger.error(f"Erro no teste de autenticação: {str(e)}")
        return jsonify({"error": "Erro interno do servidor"}), 500

