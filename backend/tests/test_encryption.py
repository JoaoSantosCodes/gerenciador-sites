import pytest
from backend.crypto.encryption import encryption_service
from backend.auth.auth_service import create_user, authenticate_user, change_master_password
from backend.database.credential_service import add_credential, list_credentials
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

def test_encryption_service():
    # Test basic encryption/decryption
    test_data = "sensitive_data"
    encryption_service.initialize("test_password")
    encrypted = encryption_service.encrypt(test_data)
    assert encrypted != test_data  # Ensure data is actually encrypted
    decrypted = encryption_service.decrypt(encrypted)
    assert decrypted == test_data  # Ensure we can decrypt correctly

def test_credential_encryption():
    # Test encryption in the context of credentials
    create_user("testuser", "masterpass")
    authenticate_user("testuser", "masterpass")
    
    # Add a credential
    user_id = SessionLocal().query(User).filter_by(username="testuser").first().id
    add_credential(user_id, "TestSite", "http://test.com", "testuser", "testpass", "test notes")
    
    # Verify the credential is stored encrypted
    session = SessionLocal()
    cred = session.query(Credential).filter_by(user_id=user_id).first()
    assert cred.password != "testpass"  # Password should be encrypted
    assert cred.notes != "test notes"   # Notes should be encrypted
    session.close()
    
    # Verify we can decrypt it
    creds = list_credentials(user_id)
    assert creds[0]['password'] == "testpass"
    assert creds[0]['notes'] == "test notes"

def test_master_password_change():
    # Test changing master password and re-encryption
    create_user("testuser", "oldpass")
    authenticate_user("testuser", "oldpass")
    
    # Add some credentials
    user_id = SessionLocal().query(User).filter_by(username="testuser").first().id
    add_credential(user_id, "Site1", "http://site1.com", "user1", "pass1", "notes1")
    add_credential(user_id, "Site2", "http://site2.com", "user2", "pass2", "notes2")
    
    # Change master password
    assert change_master_password("testuser", "oldpass", "newpass")
    
    # Verify we can still access credentials with new password
    authenticate_user("testuser", "newpass")
    creds = list_credentials(user_id)
    assert len(creds) == 2
    assert creds[0]['password'] == "pass1"
    assert creds[1]['password'] == "pass2"
    
    # Verify old password no longer works
    assert not authenticate_user("testuser", "oldpass")

def test_encryption_isolation():
    # Test that users can't access each other's credentials
    create_user("user1", "pass1")
    create_user("user2", "pass2")
    
    # Add credentials for both users
    user1_id = SessionLocal().query(User).filter_by(username="user1").first().id
    user2_id = SessionLocal().query(User).filter_by(username="user2").first().id
    
    add_credential(user1_id, "Site1", "http://site1.com", "user1", "pass1", "notes1")
    add_credential(user2_id, "Site2", "http://site2.com", "user2", "pass2", "notes2")
    
    # Verify each user can only see their own credentials
    authenticate_user("user1", "pass1")
    user1_creds = list_credentials(user1_id)
    assert len(user1_creds) == 1
    assert user1_creds[0]['username'] == "user1"
    
    authenticate_user("user2", "pass2")
    user2_creds = list_credentials(user2_id)
    assert len(user2_creds) == 1
    assert user2_creds[0]['username'] == "user2" 