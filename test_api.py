import requests
import json
import sys
from datetime import datetime

# Configurações
BASE_URL = 'http://localhost:5000/api'
TOKEN = None

# Cores para saída no terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(50)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}\n")

def print_result(success, message):
    if success:
        print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")

def login():
    global TOKEN
    print_header("Teste de Autenticação")
    
    # Teste de login
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "owner@tilesystem.com",
            "password": "password123"
        })
        
        if response.status_code == 200:
            data = response.json()
            TOKEN = data.get('access_token')
            print_result(True, f"Login bem-sucedido. Token obtido: {TOKEN[:10]}...")
            return True
        else:
            print_result(False, f"Falha no login. Status: {response.status_code}, Resposta: {response.text}")
            return False
    except Exception as e:
        print_result(False, f"Erro ao tentar login: {str(e)}")
        return False

def test_clients():
    print_header("Teste de API de Clientes")
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Teste de listagem de clientes
    try:
        response = requests.get(f"{BASE_URL}/clients", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Listagem de clientes bem-sucedida. Total: {data.get('count')}")
        else:
            print_result(False, f"Falha na listagem de clientes. Status: {response.status_code}")
    except Exception as e:
        print_result(False, f"Erro ao listar clientes: {str(e)}")
    
    # Teste de criação de cliente
    try:
        new_client = {
            "name": "Cliente de Teste",
            "email": "teste@gmail.com",
            "phone": "555-123-4567",
            "address": "123 Test St",
            "city": "Test City",
            "state": "FL",
            "zip_code": "12345",
            "referral_source": "Teste Automatizado"
        }
        
        response = requests.post(f"{BASE_URL}/clients", headers=headers, json=new_client)
        if response.status_code == 201:
            data = response.json()
            client_id = data.get('client', {}).get('id')
            print_result(True, f"Cliente criado com sucesso. ID: {client_id}")
            
            # Teste de obtenção de cliente específico
            response = requests.get(f"{BASE_URL}/clients/{client_id}", headers=headers)
            if response.status_code == 200:
                print_result(True, f"Obtenção de cliente específico bem-sucedida.")
            else:
                print_result(False, f"Falha na obtenção de cliente específico. Status: {response.status_code}")
            
            # Teste de atualização de cliente
            update_data = {"name": "Cliente de Teste Atualizado"}
            response = requests.put(f"{BASE_URL}/clients/{client_id}", headers=headers, json=update_data)
            if response.status_code == 200:
                print_result(True, f"Atualização de cliente bem-sucedida.")
            else:
                print_result(False, f"Falha na atualização de cliente. Status: {response.status_code}")
            
            # Teste de exclusão de cliente
            response = requests.delete(f"{BASE_URL}/clients/{client_id}", headers=headers)
            if response.status_code == 200:
                print_result(True, f"Exclusão de cliente bem-sucedida.")
            else:
                print_result(False, f"Falha na exclusão de cliente. Status: {response.status_code}")
        else:
            print_result(False, f"Falha na criação de cliente. Status: {response.status_code}, Resposta: {response.text}")
    except Exception as e:
        print_result(False, f"Erro nos testes de cliente: {str(e)}")

def test_projects():
    print_header("Teste de API de Projetos")
    
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Teste de listagem de projetos
    try:
        response = requests.get(f"{BASE_URL}/projects", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print_result(True, f"Listagem de projetos bem-sucedida. Total: {data.get('count')}")
        else:
            print_result(False, f"Falha na listagem de projetos. Status: {response.status_code}")
    except Exception as e:
        print_result(False, f"Erro ao listar projetos: {str(e)}")
    
    # Obter um cliente para associar ao projeto
    try:
        response = requests.get(f"{BASE_URL}/clients", headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get('count') > 0:
                client_id = data.get('clients')[0].get('id')
                
                # Teste de criação de projeto
                new_project = {
                    "client_id": client_id,
                    "title": "Projeto de Teste",
                    "project_type": "residential",
                    "status": "estimate",
                    "installation_address": "123 Test St",
                    "installation_city": "Test City",
                    "installation_state": "FL",
                    "installation_zip": "12345",
                    "estimated_start_date": datetime.now().strftime("%Y-%m-%d"),
                    "estimated_end_date": datetime.now().strftime("%Y-%m-%d"),
                    "estimated_total": "1000.00"
                }
                
                response = requests.post(f"{BASE_URL}/projects", headers=headers, json=new_project)
                if response.status_code == 201:
                    data = response.json()
                    project_id = data.get('project', {}).get('id')
                    print_result(True, f"Projeto criado com sucesso. ID: {project_id}")
                    
                    # Teste de obtenção de projeto específico
                    response = requests.get(f"{BASE_URL}/projects/{project_id}", headers=headers)
                    if response.status_code == 200:
                        print_result(True, f"Obtenção de projeto específico bem-sucedida.")
                    else:
                        print_result(False, f"Falha na obtenção de projeto específico. Status: {response.status_code}")
                    
                    # Teste de atualização de projeto
                    update_data = {"title": "Projeto de Teste Atualizado"}
                    response = requests.put(f"{BASE_URL}/projects/{project_id}", headers=headers, json=update_data)
                    if response.status_code == 200:
                        print_result(True, f"Atualização de projeto bem-sucedida.")
                    else:
                        print_result(False, f"Falha na atualização de projeto. Status: {response.status_code}")
                    
                    # Teste de exclusão de projeto
                    response = requests.delete(f"{BASE_URL}/projects/{project_id}", headers=headers)
                    if response.status_code == 200:
                        print_result(True, f"Exclusão de projeto bem-sucedida.")
                    else:
                        print_result(False, f"Falha na exclusão de projeto. Status: {response.status_code}")
                else:
                    print_result(False, f"Falha na criação de projeto. Status: {response.status_code}, Resposta: {response.text}")
            else:
                print_result(False, "Não há clientes disponíveis para criar um projeto.")
        else:
            print_result(False, f"Falha ao obter clientes para teste de projetos. Status: {response.status_code}")
    except Exception as e:
        print_result(False, f"Erro nos testes de projeto: {str(e)}")

def run_tests():
    if not login():
        print_result(False, "Testes abortados devido a falha no login.")
        return
    
    test_clients()
    test_projects()
    
    print_header("Resumo dos Testes")
    print("Testes concluídos. Verifique os resultados acima.")

if __name__ == "__main__":
    run_tests()

