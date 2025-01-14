from db import get_setting, set_setting
from crypto import derive_key
import bcrypt

def set_master_key(master_key):
    """Establece la clave maestra inicial."""
    hashed_key = bcrypt.hashpw(master_key.encode(), bcrypt.gensalt())
    set_setting("master_key", hashed_key.decode())

def validate_master_key(master_key):
    """Valida la clave maestra ingresada."""
    stored_key = get_setting("master_key")
    if not stored_key:
        return False
    return bcrypt.checkpw(master_key.encode(), stored_key.encode())
