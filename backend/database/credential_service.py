from backend.database.models import Credential, SessionLocal
from backend.crypto.crypto_service import encrypt, decrypt
from sqlalchemy.orm import Session
from datetime import datetime

# Placeholder para criptografia (implementar depois)
def encrypt_password(password: str) -> str:
    return password[::-1]  # Exemplo simples, substituir por AES depois

def decrypt_password(password_encrypted: str) -> str:
    return password_encrypted[::-1]  # Exemplo simples, substituir por AES depois


def add_credential(user_id: int, site_name: str, url: str, username: str, password: str, notes: str = ""):
    session = SessionLocal()
    password_encrypted = encrypt(password)
    cred = Credential(
        user_id=user_id,
        site_name=site_name,
        url=url,
        username=username,
        password_encrypted=password_encrypted,
        notes=notes,
        last_modified=datetime.utcnow()
    )
    session.add(cred)
    session.commit()
    session.close()


def list_credentials(user_id: int):
    session = SessionLocal()
    creds = session.query(Credential).filter_by(user_id=user_id).all()
    result = []
    for c in creds:
        try:
            password = decrypt(c.password_encrypted)
        except Exception:
            password = "[ERRO NA CRIPTOGRAFIA]"
        result.append({
            'id': c.id,
            'site_name': c.site_name,
            'url': c.url,
            'username': c.username,
            'password': password,
            'notes': c.notes
        })
    session.close()
    return result


def update_credential(cred_id: int, user_id: int, **kwargs):
    session = SessionLocal()
    cred = session.query(Credential).filter_by(id=cred_id, user_id=user_id).first()
    if not cred:
        session.close()
        return False
    for key, value in kwargs.items():
        if key == 'password':
            setattr(cred, 'password_encrypted', encrypt(value))
        elif hasattr(cred, key):
            setattr(cred, key, value)
    cred.last_modified = datetime.utcnow()
    session.commit()
    session.close()
    return True


def delete_credential(cred_id: int, user_id: int):
    session = SessionLocal()
    cred = session.query(Credential).filter_by(id=cred_id, user_id=user_id).first()
    if not cred:
        session.close()
        return False
    session.delete(cred)
    session.commit()
    session.close()
    return True 