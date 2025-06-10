from backend.database.models import Credential, SessionLocal
from backend.crypto.encryption import encryption_service
from sqlalchemy.orm import Session
from datetime import datetime

# Placeholder para criptografia (implementar depois)
def encrypt_password(password: str) -> str:
    return password[::-1]  # Exemplo simples, substituir por AES depois

def decrypt_password(password_encrypted: str) -> str:
    return password_encrypted[::-1]  # Exemplo simples, substituir por AES depois


def add_credential(user_id: int, site_name: str, url: str, username: str, password: str, notes: str = "") -> bool:
    """Add a new credential with encrypted sensitive data."""
    try:
        session = SessionLocal()
        encrypted_password = encryption_service.encrypt(password)
        encrypted_notes = encryption_service.encrypt(notes) if notes else ""
        
        credential = Credential(
            user_id=user_id,
            site_name=site_name,
            url=url,
            username=username,
            password=encrypted_password,
            notes=encrypted_notes
        )
        session.add(credential)
        session.commit()
        return True
    except Exception as e:
        print(f"Error adding credential: {e}")
        return False
    finally:
        session.close()


def list_credentials(user_id: int) -> list:
    """List all credentials for a user with decrypted sensitive data."""
    try:
        session = SessionLocal()
        credentials = session.query(Credential).filter_by(user_id=user_id).all()
        return [{
            'id': c.id,
            'site_name': c.site_name,
            'url': c.url,
            'username': c.username,
            'password': encryption_service.decrypt(c.password),
            'notes': encryption_service.decrypt(c.notes) if c.notes else ""
        } for c in credentials]
    finally:
        session.close()


def update_credential(credential_id: int, user_id: int, **updates) -> bool:
    """Update a credential with encrypted sensitive data."""
    try:
        session = SessionLocal()
        credential = session.query(Credential).filter_by(id=credential_id, user_id=user_id).first()
        if not credential:
            return False

        if 'password' in updates:
            updates['password'] = encryption_service.encrypt(updates['password'])
        if 'notes' in updates:
            updates['notes'] = encryption_service.encrypt(updates['notes'])

        for key, value in updates.items():
            setattr(credential, key, value)
        
        session.commit()
        return True
    except Exception as e:
        print(f"Error updating credential: {e}")
        return False
    finally:
        session.close()


def delete_credential(credential_id: int, user_id: int) -> bool:
    """Delete a credential."""
    try:
        session = SessionLocal()
        credential = session.query(Credential).filter_by(id=credential_id, user_id=user_id).first()
        if not credential:
            return False
        
        session.delete(credential)
        session.commit()
        return True
    except Exception as e:
        print(f"Error deleting credential: {e}")
        return False
    finally:
        session.close() 