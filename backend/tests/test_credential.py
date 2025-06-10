import pytest
from backend.auth.auth_service import create_user, authenticate_user
from backend.database.credential_service import add_credential, list_credentials, update_credential, delete_credential
from backend.database.models import SessionLocal, User, Credential

def clear_all():
    session = SessionLocal()
    session.query(Credential).delete()
    session.query(User).delete()
    session.commit()
    session.close()

@pytest.fixture(autouse=True)
def run_around_tests():
    clear_all()
    yield
    clear_all()

def get_user_id(username):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user.id if user else None

def test_crud_credential():
    create_user('user1', 'pass1')
    user_id = get_user_id('user1')
    # Adicionar
    add_credential(user_id, 'SiteA', 'http://a.com', 'userA', 'senhaA', 'notaA')
    creds = list_credentials(user_id)
    assert len(creds) == 1
    assert creds[0]['site_name'] == 'SiteA'
    assert creds[0]['password'] == 'senhaA'  # Testa descriptografia
    # Editar
    cred_id = creds[0]['id']
    update_credential(cred_id, user_id, password='novaSenha', notes='novaNota')
    creds = list_credentials(user_id)
    assert creds[0]['password'] == 'novaSenha'
    assert creds[0]['notes'] == 'novaNota'
    # Excluir
    delete_credential(cred_id, user_id)
    creds = list_credentials(user_id)
    assert len(creds) == 0 