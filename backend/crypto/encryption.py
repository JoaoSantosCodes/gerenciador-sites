from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from typing import Tuple

class EncryptionService:
    def __init__(self):
        self.salt = os.urandom(16)
        self._fernet = None

    def _derive_key(self, master_password: str) -> bytes:
        """Derive encryption key from master password using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

    def initialize(self, master_password: str):
        """Initialize encryption with master password."""
        key = self._derive_key(master_password)
        self._fernet = Fernet(key)

    def encrypt(self, data: str) -> str:
        """Encrypt sensitive data."""
        if not self._fernet:
            raise ValueError("Encryption service not initialized")
        return self._fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        if not self._fernet:
            raise ValueError("Encryption service not initialized")
        return self._fernet.decrypt(encrypted_data.encode()).decode()

    def get_salt(self) -> bytes:
        """Get the salt used for key derivation."""
        return self.salt

    def set_salt(self, salt: bytes):
        """Set the salt for key derivation."""
        self.salt = salt

# Singleton instance
encryption_service = EncryptionService() 