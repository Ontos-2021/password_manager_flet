import hashlib
import base64
import random
import string
import csv
from crypto import encrypt, decrypt
from db import insert_password, fetch_passwords, delete_password


# ========================
# Generación de Contraseñas
# ========================
def generate_password(seed, platform, length=16, iterations=1, use_uppercase=True, use_lowercase=True,
                      use_digits=True, use_specials=False):
    """
    Genera una contraseña segura basada en una semilla, plataforma y configuraciones.
    """
    if length < 8:
        raise ValueError("La longitud mínima de la contraseña debe ser 8.")
    if iterations < 1:
        raise ValueError("El número de iteraciones debe ser al menos 1.")

    # Generar un hash base a partir de la semilla y la plataforma
    combined = seed + platform
    hash_object = hashlib.sha256(combined.encode())
    for _ in range(iterations - 1):
        hash_object = hashlib.sha256(hash_object.digest())

    # Base legible en base64
    base_password = base64.urlsafe_b64encode(hash_object.digest()).decode().strip('=')

    # Construir el conjunto de caracteres permitidos
    characters = ""
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_specials:
        characters += string.punctuation

    if not characters:
        raise ValueError("Debe haber al menos un tipo de carácter permitido.")

    # Generar la contraseña final usando la base_password como semilla para random
    random.seed(base_password)
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


# ========================
# Gestión de Contraseñas
# ========================
def save_password(seed, platform, description, password, iterations, master_key):
    """
    Cifra y guarda una contraseña en la base de datos.
    """
    encrypted_password = encrypt(password, master_key)  # Cifrar la contraseña
    insert_password(seed, platform, description, encrypted_password, iterations)  # Guardar en la base de datos


def get_passwords(master_key):
    """
    Obtiene todas las contraseñas descifradas desde la base de datos.
    """
    passwords = fetch_passwords()  # Obtiene las contraseñas cifradas
    decrypted_passwords = []
    for record in passwords:
        id_, seed, platform, description, encrypted_password, iterations, created_at = record
        try:
            decrypted_password = decrypt(encrypted_password, master_key)
            decrypted_passwords.append(
                (id_, seed, platform, description, decrypted_password.decode(), iterations, created_at))
        except Exception as e:
            decrypted_passwords.append(
                (id_, seed, platform, description, "ERROR: No se pudo descifrar", iterations, created_at))
    return decrypted_passwords


def remove_password(password_id):
    """
    Elimina una contraseña de la base de datos.
    """
    delete_password(password_id)


# ========================
# Importar Contraseñas
# ========================
def import_passwords_from_csv(master_key, file_path):
    """
    Importa contraseñas desde un archivo CSV.
    """
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Validar que las columnas requeridas estén presentes
                if "Semilla" in row and "Plataforma" in row and "Descripción" in row and "Contraseña" in row and "Iteraciones" in row:
                    encrypted_password = encrypt(row["Contraseña"], master_key)  # Cifrar la contraseña
                    insert_password(
                        row["Semilla"],
                        row["Plataforma"],
                        row["Descripción"],
                        encrypted_password,  # Contraseña cifrada
                        int(row["Iteraciones"])
                    )
                else:
                    raise ValueError("El archivo CSV no contiene las columnas requeridas.")
    except Exception as e:
        raise Exception(f"Error al procesar el archivo CSV: {e}")


# ========================
# Exportar Contraseñas
# ========================
def export_passwords_to_csv(master_key, file_path):
    """
    Exporta contraseñas descifradas a un archivo CSV.
    """
    try:
        passwords = get_passwords(master_key)  # Obtiene contraseñas descifradas
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # Escribir encabezados
            writer.writerow(["Semilla", "Plataforma", "Descripción", "Contraseña", "Iteraciones", "Fecha de Creación"])
            # Escribir datos
            for _, seed, platform, description, password, iterations, created_at in passwords:
                writer.writerow([seed, platform, description, password, iterations, created_at])
    except Exception as e:
        raise Exception(f"Error al exportar contraseñas: {e}")
