from cryptography.fernet import Fernet
import base64

def generate_key():
    master_key = Fernet.generate_key()
    fernet = Fernet(master_key)
    secret_key = Fernet.generate_key()
    encrypted_secret_key = fernet.encrypt(secret_key)
    
    return master_key, encrypted_secret_key

def main():
    master_key, encrypted_secret_key = generate_key()
    print(f"Master Key: {master_key.decode()}")
    print(f"Encrypted Secret Key: {encrypted_secret_key.decode()}")

if __name__ == "__main__":
    main()


