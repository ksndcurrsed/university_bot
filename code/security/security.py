import os
from cryptography.fernet import Fernet
import base64

class security:
    def __init__(self):
        self.master_key = os.getenv('MASTER_KEY')
        encrypted_key = os.getenv('SEKRET_KEY')
        self.key = self.decrypt_key(self.master_key, encrypted_key)

    def decrypt_key(self, master_key, encrypted_secret_key):
        master_key = self.master_key.encode()
        encrypted_secret_key = encrypted_secret_key.encode()
        
        fernet = Fernet(master_key)
        
        secret_key = fernet.decrypt(encrypted_secret_key)
        return secret_key

    def encrypt(self, logdata):
        fernet = Fernet(self.key)
        encrypted_data = fernet.encrypt(logdata.encode())
        return encrypted_data

    def decrypt(self, encrypted_data):
        fernet = Fernet(self.key)
        decrypted_data = fernet.decrypt(encrypted_data).decode()
        return decrypted_data
    


