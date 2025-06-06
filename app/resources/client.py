from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app import db
from app.models.client import Client
from app.schemas import ClientSchema, ClientUpdateSchema

client_bp = Blueprint('client', __name__)
client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
client_update_schema = ClientUpdateSchema()

@client_bp.route('', methods=['POST'])
@jwt_required()
def create_client():
    """Cria um novo cliente"""
    try:
        data = client_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"message": "Erro de validação", "errors": err.messages}), 400
    
    # Cria um novo cliente
    client = Client(**data)
    
    # Salva o cliente no banco de dados
    db.session.add(client)
    db.session.commit()
    
    return jsonify({
        "message": "Cliente criado com sucesso",
        "client": client_schema.dump(client)
    }), 201

@client_bp.route('', methods=['GET'])
@jwt_required()
def get_clients():
    """Retorna todos os clientes ativos"""
    # Parâmetros de consulta para filtragem
    name = request.args.get('name')
    phone = request.args.get('phone')
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    
    # Consulta base
    query = Client.query
    
    # Aplica filtros se fornecidos
    if name:
        query = query.filter(Client.name.ilike(f'%{name}%'))
    if phone:
        query = query.filter(Client.phone.ilike(f'%{phone}%'))
    if active_only:
        query = query.filter_by(active=True)
    
    # Ordena por nome
    clients = query.order_by(Client.name).all()
    
    return jsonify({
        "clients": clients_schema.dump(clients),
        "count": len(clients)
    }), 200

@client_bp.route('/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client(client_id):
    """Retorna um cliente específico"""
    client = Client.query.get_or_404(client_id)
    
    return jsonify({
        "client": client_schema.dump(client)
    }), 200

@client_bp.route('/<int:client_id>', methods=['PUT'])
@jwt_required()
def update_client(client_id):
    """Atualiza um cliente existente"""
    client = Client.query.get_or_404(client_id)
    
    try:
        data = client_update_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"message": "Erro de validação", "errors": err.messages}), 400
    
    # Atualiza os campos do cliente
    for key, value in data.items():
        setattr(client, key, value)
    
    # Salva as alterações
    db.session.commit()
    
    return jsonify({
        "message": "Cliente atualizado com sucesso",
        "client": client_schema.dump(client)
    }), 200

@client_bp.route('/<int:client_id>', methods=['DELETE'])
@jwt_required()
def delete_client(client_id):
    """Desativa um cliente (soft delete)"""
    client = Client.query.get_or_404(client_id)
    
    # Verifica se o cliente tem projetos ativos
    if client.projects.filter_by(status='in_progress').first():
        return jsonify({
            "message": "Não é possível excluir um cliente com projetos em andamento"
        }), 400
    
    # Soft delete - apenas marca como inativo
    client.active = False
    db.session.commit()
    
    return jsonify({
        "message": "Cliente desativado com sucesso"
    }), 200

