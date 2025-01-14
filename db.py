import sqlite3

DB_FILE = "password_manager.db"

def init_db():
    """Inicializa la base de datos y crea las tablas necesarias."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Tabla para almacenar contraseñas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            seed TEXT NOT NULL,
            platform TEXT NOT NULL,
            description TEXT,
            password TEXT NOT NULL,
            iterations INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla para configuraciones globales
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_name TEXT NOT NULL UNIQUE,
            key_value TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def insert_password(seed, platform, description, password, iterations):
    """Inserta una contraseña en la base de datos."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO passwords (seed, platform, description, password, iterations)
        VALUES (?, ?, ?, ?, ?)
    """, (seed, platform, description, password, iterations))
    conn.commit()
    conn.close()

def fetch_passwords():
    """Obtiene todas las contraseñas de la base de datos."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM passwords")
    passwords = cursor.fetchall()
    conn.close()
    return passwords

def delete_password(password_id):
    """Elimina una contraseña de la base de datos."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM passwords WHERE id = ?", (password_id,))
    conn.commit()
    conn.close()

def get_setting(key_name):
    """Obtiene un valor de configuración."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT key_value FROM settings WHERE key_name = ?", (key_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def set_setting(key_name, key_value):
    """Establece un valor de configuración."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO settings (key_name, key_value)
        VALUES (?, ?)
        ON CONFLICT(key_name) DO UPDATE SET key_value = excluded.key_value
    """, (key_name, key_value))
    conn.commit()
    conn.close()
