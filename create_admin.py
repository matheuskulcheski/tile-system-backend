import os
import sys

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from werkzeug.security import generate_password_hash

# Cria a aplicação
app = create_app()

# Define o modelo User diretamente aqui para evitar problemas de importação
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

with app.app_context():
    try:
        # Cria as tabelas se não existirem
        db.create_all()
        print("Tabelas criadas/verificadas com sucesso!")
        
        # Dados do usuário administrador
        admin_email = "admin@empresa.com"
        admin_password = "123456"
        admin_nome = "Administrador"
        
        # Verifica se o usuário já existe
        existing_user = User.query.filter_by(email=admin_email).first()
        
        if existing_user:
            print(f"Usuário já existe: {existing_user.email}")
            print("Atualizando senha...")
            existing_user.password = generate_password_hash(admin_password)
            db.session.commit()
            print("Senha atualizada com sucesso!")
        else:
            # Cria o novo usuário
            admin_user = User(
                nome=admin_nome,
                email=admin_email,
                password=generate_password_hash(admin_password),
                role="admin"
            )
            
            db.session.add(admin_user)
            db.session.commit()
            print(f"Usuário administrador criado com sucesso! ID: {admin_user.id}")
        
        # Lista todos os usuários
        print("\nLista de todos os usuários:")
        users = User.query.all()
        for user in users:
            print(f"ID: {user.id}, Nome: {user.nome}, Email: {user.email}, Role: {user.role}")
        
        print(f"\nTotal de usuários: {len(users)}")
        
    except Exception as e:
        print(f"Erro: {str(e)}")
        import traceback
        traceback.print_exc()

