from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from app import db
from app.models.project import Project
from app.models.client import Client
from app.schemas import ProjectSchema, ProjectUpdateSchema

project_bp = Blueprint('project', __name__)
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)
project_update_schema = ProjectUpdateSchema()

@project_bp.route('', methods=['POST'])
@jwt_required()
def create_project():
    """Cria um novo projeto"""
    try:
        data = project_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"message": "Erro de validação", "errors": err.messages}), 400
    
    # Verifica se o cliente existe
    client = Client.query.get(data['client_id'])
    if not client:
        return jsonify({"message": "Cliente não encontrado"}), 404
    
    # Cria um novo projeto
    project = Project(**data)
    
    # Salva o projeto no banco de dados
    db.session.add(project)
    db.session.commit()
    
    return jsonify({
        "message": "Projeto criado com sucesso",
        "project": project_schema.dump(project)
    }), 201

@project_bp.route('', methods=['GET'])
@jwt_required()
def get_projects():
    """Retorna todos os projetos"""
    # Parâmetros de consulta para filtragem
    client_id = request.args.get('client_id', type=int)
    status = request.args.get('status')
    project_type = request.args.get('project_type')
    
    # Consulta base
    query = Project.query
    
    # Aplica filtros se fornecidos
    if client_id:
        query = query.filter_by(client_id=client_id)
    if status:
        query = query.filter_by(status=status)
    if project_type:
        query = query.filter_by(project_type=project_type)
    
    # Ordena por data de criação (mais recente primeiro)
    projects = query.order_by(Project.created_at.desc()).all()
    
    return jsonify({
        "projects": projects_schema.dump(projects),
        "count": len(projects)
    }), 200

@project_bp.route('/<int:project_id>', methods=['GET'])
@jwt_required()
def get_project(project_id):
    """Retorna um projeto específico"""
    project = Project.query.get_or_404(project_id)
    
    return jsonify({
        "project": project_schema.dump(project)
    }), 200

@project_bp.route('/<int:project_id>', methods=['PUT'])
@jwt_required()
def update_project(project_id):
    """Atualiza um projeto existente"""
    project = Project.query.get_or_404(project_id)
    
    try:
        data = project_update_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"message": "Erro de validação", "errors": err.messages}), 400
    
    # Verifica se o cliente existe, se fornecido
    if 'client_id' in data:
        client = Client.query.get(data['client_id'])
        if not client:
            return jsonify({"message": "Cliente não encontrado"}), 404
    
    # Atualiza os campos do projeto
    for key, value in data.items():
        setattr(project, key, value)
    
    # Salva as alterações
    db.session.commit()
    
    return jsonify({
        "message": "Projeto atualizado com sucesso",
        "project": project_schema.dump(project)
    }), 200

@project_bp.route('/<int:project_id>', methods=['DELETE'])
@jwt_required()
def delete_project(project_id):
    """Cancela um projeto"""
    project = Project.query.get_or_404(project_id)
    
    # Verifica se o projeto já está concluído ou cancelado
    if project.status in ['completed', 'cancelled']:
        return jsonify({
            "message": f"Não é possível excluir um projeto que já está {project.status}"
        }), 400
    
    # Marca o projeto como cancelado
    project.status = 'cancelled'
    db.session.commit()
    
    return jsonify({
        "message": "Projeto cancelado com sucesso"
    }), 200

@project_bp.route('/client/<int:client_id>', methods=['GET'])
@jwt_required()
def get_client_projects(client_id):
    """Retorna todos os projetos de um cliente específico"""
    # Verifica se o cliente existe
    client = Client.query.get_or_404(client_id)
    
    # Obtém os projetos do cliente
    projects = Project.query.filter_by(client_id=client_id).order_by(Project.created_at.desc()).all()
    
    return jsonify({
        "client": client.name,
        "projects": projects_schema.dump(projects),
        "count": len(projects)
    }), 200

