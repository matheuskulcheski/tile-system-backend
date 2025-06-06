import os
from dotenv import load_dotenv
from app import create_app, db

# Carrega variáveis de ambiente do arquivo .env se existir
load_dotenv()

# Cria a aplicação com a configuração apropriada
app = create_app(os.getenv('FLASK_CONFIG', 'default'))

@app.shell_context_processor
def make_shell_context():
    """Adiciona objetos ao contexto do shell Flask"""
    return {'db': db}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

