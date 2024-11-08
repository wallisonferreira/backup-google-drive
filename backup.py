import os
import re
import argparse
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Configurações de autenticação e acesso à API
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Inicialização do serviço Google Drive API
service = build('drive', 'v3', credentials=credentials)

# Função para extrair o ID de uma pasta a partir de um link
def extract_folder_id(link):
    match = re.search(r'\/folders\/([a-zA-Z0-9_-]+)', link)
    return match.group(1) if match else None

# Função para listar arquivos e pastas dentro de uma pasta
def list_items_in_folder(folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    try:
        results = service.files().list(q=query).execute()
        items = results.get('files', [])
        return items
    except Exception as e:
        print(f"Erro ao listar itens na pasta {folder_id}: {e}")
        return []

# Função para buscar um item pelo nome na pasta de destino
def find_item_in_folder(item_name, folder_id):
    query = f"'{folder_id}' in parents and name = '{item_name}' and trashed = false"
    try:
        results = service.files().list(q=query).execute()
        items = results.get('files', [])
        return items[0] if items else None
    except Exception as e:
        print(f"Erro ao buscar o item '{item_name}' na pasta {folder_id}: {e}")
        return None

# Função para criar uma pasta na pasta de destino, mantendo a hierarquia
def create_folder(folder_name, parent_folder_id):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    try:
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        print(f"Pasta criada: {folder_name} -> ID: {folder['id']}")
        return folder['id']
    except Exception as e:
        print(f"Erro ao criar a pasta '{folder_name}': {e}")
        return None

# Função para copiar arquivo para a pasta de destino
def copy_file(file_id, dest_folder_id, file_name):
    copied_file = {
        'name': file_name,
        'parents': [dest_folder_id]
    }
    try:
        return service.files().copy(fileId=file_id, body=copied_file).execute()
    except Exception as e:
        print(f"Erro ao copiar o arquivo '{file_name}' com ID {file_id}: {e}")
        return None

# Função recursiva para espelhar a estrutura de pastas e arquivos
def mirror_folder_structure(source_folder_id, dest_folder_id):
    items = list_items_in_folder(source_folder_id)

    for item in items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            # Verifica se a pasta já existe no destino
            existing_folder = find_item_in_folder(item['name'], dest_folder_id)
            if existing_folder:
                print(f"Pasta já existe: {item['name']} -> ID: {existing_folder['id']}")
                mirror_folder_structure(item['id'], existing_folder['id'])
            else:
                new_dest_folder_id = create_folder(item['name'], dest_folder_id)
                if new_dest_folder_id:
                    mirror_folder_structure(item['id'], new_dest_folder_id)
        else:
            existing_file = find_item_in_folder(item['name'], dest_folder_id)
            if existing_file:
                print(f"Arquivo já existe e será ignorado: {item['name']}")
            else:
                copy_file(item['id'], dest_folder_id, item['name'])

# Configuração de argumentos de linha de comando
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Realizar backup de pastas e arquivos do Google Drive mantendo a hierarquia.")
    parser.add_argument("--source_link", required=True, help="Link da pasta de origem")
    parser.add_argument("--destination_link", required=True, help="Link da pasta de destino")
    args = parser.parse_args()

    # Extrai os IDs das pastas a partir dos links fornecidos
    SOURCE_FOLDER_ID = extract_folder_id(args.source_link)
    DESTINATION_FOLDER_ID = extract_folder_id(args.destination_link)

    if not SOURCE_FOLDER_ID or not DESTINATION_FOLDER_ID:
        print("Erro: Não foi possível extrair os IDs das pastas a partir dos links fornecidos.")
    else:
        mirror_folder_structure(SOURCE_FOLDER_ID, DESTINATION_FOLDER_ID)
