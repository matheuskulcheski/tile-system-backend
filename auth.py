from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registra um novo usuário"""
    data = request.get_json()
    
    # Verifica se o email já está em uso
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'Email já está em uso'}), 400
    
    # Cria um novo usuário
    user = User(
        name=data.get('name'),
        email=data.get('email'),
        role=data.get('role', 'installer'),  # Default para instalador
        phone=data.get('phone')
    )
    user.password = data.get('password')  # Usa o setter para gerar o hash
    
    # Salva o usuário no banco de dados
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuário registrado com sucesso', 'user': user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Autentica um usuário e retorna um token JWT"""
    data = request.get_json()
    
    # Busca o usuário pelo email
    user = User.query.filter_by(email=data.get('email')).first()
    
    # Verifica se o usuário existe e a senha está correta
    if not user or not user.verify_password(data.get('password')):
        return jsonify({'message': 'Email ou senha inválidos'}), 401
    
    # Verifica se o usuário está ativo
    if not user.active:
        return jsonify({'message': 'Conta desativada. Entre em contato com o administrador'}), 401
    
    # Gera o token JWT
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login realizado com sucesso',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    """Retorna os dados do usuário autenticado"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    return jsonify({'user': user.to_dict()}), 200

@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    """Altera a senha do usuário autenticado"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado'}), 404
    
    data = request.get_json()
    
    # Verifica se a senha atual está correta
    if not user.verify_password(data.get('current_password')):
        return jsonify({'message': 'Senha atual incorreta'}), 400
    
    # Altera a senha
    user.password = data.get('new_password')
    db.session.commit()
    
    return jsonify({'message': 'Senha alterada com sucesso'}), 200

