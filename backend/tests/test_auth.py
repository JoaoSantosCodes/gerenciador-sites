import pytest
from backend.auth.auth_service import create_user, authenticate_user
from backend.database.models import SessionLocal, User

def clear_users():
    session = SessionLocal()
    session.query(User).delete()
    session.commit()
    session.close()

@pytest.fixture(autouse=True)
def run_around_tests():
    clear_users()
    yield
    clear_users()

def test_create_user():
    assert create_user('testuser', 'testpass') is True
    # Não permite duplicado
    assert create_user('testuser', 'testpass') is False

def test_authenticate_user():
    create_user('testuser', 'testpass')
    assert authenticate_user('testuser', 'testpass') is True
    assert authenticate_user('testuser', 'wrongpass') is False
    assert authenticate_user('wronguser', 'testpass') is False 