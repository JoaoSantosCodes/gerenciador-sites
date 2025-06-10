from backend.database.models import User, SessionLocal, init_db
from sqlalchemy.exc import IntegrityError
import bcrypt

init_db()

def create_user(username: str, password: str) -> bool:
    session = SessionLocal()
    try:
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = User(username=username, password_hash=password_hash.decode('utf-8'))
        session.add(user)
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False  # Usuário já existe
    finally:
        session.close()

def authenticate_user(username: str, password: str) -> bool:
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return True
    return False 