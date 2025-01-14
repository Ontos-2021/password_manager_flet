import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

SALT_SIZE = 16
KEY_SIZE = 32
ITERATIONS = 100_000


def derive_key(master_key, salt):
    """Deriva una clave simétrica usando PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(master_key.encode())


def encrypt(data, master_key):
    """Cifra los datos usando una clave derivada."""
    salt = os.urandom(SALT_SIZE)
    key = derive_key(master_key, salt)
    iv = os.urandom(16)  # Vector de inicialización
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
    return base64.urlsafe_b64encode(salt + iv + ciphertext).decode()


def decrypt(token, master_key):
    """Descifra los datos usando la clave derivada."""
    decoded = base64.urlsafe_b64decode(token)
    salt = decoded[:SALT_SIZE]
    iv = decoded[SALT_SIZE:SALT_SIZE + 16]
    ciphertext = decoded[SALT_SIZE + 16:]
    key = derive_key(master_key, salt)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()
