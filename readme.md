# Configurando o Ambiente Python

## 1. Clone o Projeto
Clone o projeto para o seu ambiente local com o seguinte comando:

```bash
git clone https://github.com/wallisonferreira/backup-google-drive
```

## 2. Crie o Ambiente Virtual
No diretório do projeto, crie um ambiente virtual com o seguinte comando:

```bash
python -m venv .venv
```

## 3. Ative o Ambiente Virtual
Ative o ambiente virtual. O comando depende do seu sistema operacional:

### Windows
```bash
.venv\Scripts\activate
```
### Linux
```bash
source .venv/bin/activate
```

## 4. Instale as Dependências
Instale todas as dependências listadas no arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

## 5. Configure o Ambiente do Google Cloud Console
Acesse o Google Cloud Console para criar uma Conta de Serviço. Baixe o arquivo credentials.json da Conta de Serviço e coloque-o na raiz do projeto.

## 6. Configure a Conta de Serviço
No Google Cloud Console, adicione a Conta de Serviço como membro com permissões de edição nos diretórios de origem e destino que você deseja acessar.

Exemplo de Conta de Serviço: meu-app-backup-drive@gothic-calling-441022-s2.iam.gserviceaccount.com

## 7. Execute o Programa
Com o credentials.json na raiz do projeto, execute o programa usando o seguinte comando:

```bash
python backup.py --source_link="https://drive.google.com/drive/folders/113SDbpCFsgiZ0hYiVv0OHmJv4oO0Fd44?hl=pt-BR" --destination_link="https://drive.google.com/drive/folders/1hcPt_uMh9JeLm-e-8qobg9hHrMSFg755?hl=pt-BR"
```

### Certifique-se de substituir os links de source_link e destination_link pelos links das pastas do Google Drive que você deseja usar.