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
    print(f"Derivando clave con salt: {base64.urlsafe_b64encode(salt).decode()}")
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
    print("Iniciando cifrado de datos.")
    salt = os.urandom(SALT_SIZE)  # Genera un salt único para cada operación
    print(f"Salt generado: {base64.urlsafe_b64encode(salt).decode()}")
    key = derive_key(master_key, salt)  # Deriva la clave usando PBKDF2
    iv = os.urandom(16)  # Vector de inicialización único
    print(f"Vector de inicialización (IV) generado: {base64.urlsafe_b64encode(iv).decode()}")
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data.encode()) + encryptor.finalize()
    print("Cifrado exitoso.")

    # Devuelve el salt, iv, ciphertext y tag en un solo token codificado
    encrypted_data = base64.urlsafe_b64encode(salt + iv + ciphertext + encryptor.tag).decode()
    print(f"Datos cifrados generados: {encrypted_data}")
    return encrypted_data


def decrypt(token, master_key):
    """Descifra los datos usando la clave derivada."""
    print("Iniciando descifrado de datos.")
    decoded = base64.urlsafe_b64decode(token)
    salt = decoded[:SALT_SIZE]  # Extrae el salt
    print(f"Salt extraído: {base64.urlsafe_b64encode(salt).decode()}")
    iv = decoded[SALT_SIZE:SALT_SIZE + 16]  # Extrae el IV
    print(f"Vector de inicialización (IV) extraído: {base64.urlsafe_b64encode(iv).decode()}")
    ciphertext = decoded[SALT_SIZE + 16:-16]  # Extrae el texto cifrado
    tag = decoded[-16:]  # Extrae el tag de autenticación
    print(f"Tag de autenticación extraído: {base64.urlsafe_b64encode(tag).decode()}")

    key = derive_key(master_key, salt)  # Deriva la clave usando el mismo salt
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        print("Descifrado exitoso.")
        return decrypted_data
    except Exception as e:
        print(f"Error al descifrar: {e}")
        raise
