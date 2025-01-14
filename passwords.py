import hashlib
import base64
import random
import string
from crypto import encrypt, decrypt
from db import insert_password, fetch_passwords, delete_password


def generate_password(seed, platform, length=16, iterations=1, use_uppercase=True, use_lowercase=True, use_digits=True,
                      use_specials=False):
    """
    Genera una contraseña segura basada en una semilla, plataforma y configuraciones.
    - seed: Semilla (palabra clave) para la generación de la contraseña.
    - platform: Plataforma asociada a la contraseña (ej., Gmail, Facebook).
    - length: Longitud de la contraseña generada.
    - iterations: Número de iteraciones del algoritmo de hash.
    - use_uppercase, use_lowercase, use_digits, use_specials: Tipos de caracteres a incluir.
    """
    if length < 8:
        raise ValueError("La longitud mínima de la contraseña debe ser 8")
    if iterations < 1:
        raise ValueError("El número de iteraciones debe ser al menos 1")

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


def save_password(seed, platform, description, password, iterations, master_key):
    """
    Cifra y guarda una contraseña en la base de datos.
    - seed: Semilla utilizada para la generación.
    - platform: Plataforma asociada.
    - description: Descripción opcional.
    - password: Contraseña generada (sin cifrar).
    - iterations: Número de iteraciones utilizadas.
    - master_key: Clave maestra para el cifrado.
    """
    encrypted_password = encrypt(password, master_key)  # Cifrar la contraseña
    insert_password(seed, platform, description, encrypted_password, iterations)  # Guardar en la base de datos


def get_passwords(master_key):
    """
    Obtiene todas las contraseñas descifradas desde la base de datos.
    - master_key: Clave maestra para descifrar las contraseñas.
    - Retorna: Una lista de tuplas con los registros descifrados.
    """
    passwords = fetch_passwords()
    decrypted_passwords = []
    for record in passwords:
        id_, seed, platform, description, encrypted_password, iterations, created_at = record
        try:
            decrypted_password = decrypt(encrypted_password, master_key)
            decrypted_passwords.append(
                (id_, seed, platform, description, decrypted_password.decode(), iterations, created_at))
        except Exception:
            decrypted_passwords.append(
                (id_, seed, platform, description, "ERROR: No se pudo descifrar", iterations, created_at))
    return decrypted_passwords


def remove_password(password_id):
    """
    Elimina una contraseña de la base de datos.
    - password_id: ID del registro a eliminar.
    """
    delete_password(password_id)


import csv
from db import insert_password


def import_passwords_from_csv(master_key, file_path):
    """
    Importa contraseñas desde un archivo CSV.
    - master_key: Clave maestra para cifrar las contraseñas.
    - file_path: Ruta del archivo CSV.
    """
    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Validar que las columnas requeridas estén presentes
                if "Semilla" in row and "Plataforma" in row and "Descripción" in row and "Contraseña" in row and "Iteraciones" in row:
                    insert_password(
                        row["Semilla"],
                        row["Plataforma"],
                        row["Descripción"],
                        row["Contraseña"],  # Almacena cifrada
                        int(row["Iteraciones"])
                    )
                else:
                    raise ValueError("El archivo CSV no contiene las columnas requeridas.")
    except Exception as e:
        raise Exception(f"Error al procesar el archivo CSV: {e}")

import csv
from passwords import get_passwords  # Lógica para obtener contraseñas desde la base de datos

def export_passwords_to_csv(master_key, file_path):
    """
    Exporta contraseñas descifradas a un archivo CSV.
    - master_key: Clave maestra para descifrar las contraseñas.
    - file_path: Ruta del archivo CSV de destino.
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
