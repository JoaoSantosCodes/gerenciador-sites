import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

KEY_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', '.env')
FERNET_KEY = os.getenv('FERNET_KEY')

# Gera e salva uma chave se não existir
if not FERNET_KEY:
    key = Fernet.generate_key()
    with open(KEY_PATH, 'a') as f:
        f.write(f'FERNET_KEY={key.decode()}\n')
    FERNET_KEY = key.decode()

fernet = Fernet(FERNET_KEY.encode())

def encrypt(text: str) -> str:
    return fernet.encrypt(text.encode()).decode()

def decrypt(token: str) -> str:
    return fernet.decrypt(token.encode()).decode() 