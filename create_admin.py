
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

# Substitua os dados abaixo se quiser
admin_email = "admin@empresa.com"
admin_password = "123456"

# Verifica se o usuário já existe
if User.query.filter_by(email=admin_email).first():
    print("Usuário já existe.")
else:
    admin_user = User(
        nome="Administrador",
        email=admin_email,
        password=generate_password_hash(admin_password),
        role="admin"
    )
    db.session.add(admin_user)
    db.session.commit()
    print("Usuário administrador criado com sucesso!")
