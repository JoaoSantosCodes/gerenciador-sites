from backend.database.models import User, SessionLocal, init_db
from sqlalchemy.exc import IntegrityError
import bcrypt
from backend.crypto.encryption import encryption_service
from datetime import datetime

init_db()

def create_user(username: str, password: str) -> bool:
    """Create a new user with hashed password and encryption salt."""
    try:
        session = SessionLocal()
        # Check if user already exists
        if session.query(User).filter_by(username=username).first():
            return False

        # Hash the password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode(), salt)

        # Create new user with encryption salt
        user = User(
            username=username,
            password_hash=password_hash.decode(),
            salt=encryption_service.get_salt().hex()
        )
        
        session.add(user)
        session.commit()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        session.close()

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate a user and initialize encryption if successful."""
    try:
        session = SessionLocal()
        user = session.query(User).filter_by(username=username).first()
        
        if not user:
            return False

        # Verify password
        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return False

        # Initialize encryption with user's salt
        encryption_service.set_salt(bytes.fromhex(user.salt))
        encryption_service.initialize(password)

        # Update last login
        user.last_login = datetime.utcnow()
        session.commit()
        
        return True
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return False
    finally:
        session.close()

def change_master_password(username: str, old_password: str, new_password: str) -> bool:
    """Change user's master password and re-encrypt all credentials."""
    try:
        session = SessionLocal()
        user = session.query(User).filter_by(username=username).first()
        
        if not user:
            return False

        # Verify old password
        if not bcrypt.checkpw(old_password.encode(), user.password_hash.encode()):
            return False

        # Initialize encryption with old password to decrypt credentials
        encryption_service.set_salt(bytes.fromhex(user.salt))
        encryption_service.initialize(old_password)

        # Get all credentials
        credentials = user.credentials
        decrypted_credentials = []
        for cred in credentials:
            decrypted_credentials.append({
                'id': cred.id,
                'site_name': cred.site_name,
                'url': cred.url,
                'username': cred.username,
                'password': encryption_service.decrypt(cred.password),
                'notes': encryption_service.decrypt(cred.notes) if cred.notes else ""
            })

        # Generate new salt and hash new password
        new_salt = encryption_service.get_salt()
        new_password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

        # Update user's password and salt
        user.password_hash = new_password_hash.decode()
        user.salt = new_salt.hex()

        # Re-encrypt all credentials with new password
        encryption_service.initialize(new_password)
        for cred in credentials:
            decrypted = next(c for c in decrypted_credentials if c['id'] == cred.id)
            cred.password = encryption_service.encrypt(decrypted['password'])
            if decrypted['notes']:
                cred.notes = encryption_service.encrypt(decrypted['notes'])

        session.commit()
        return True
    except Exception as e:
        print(f"Error changing master password: {e}")
        return False
    finally:
        session.close() 