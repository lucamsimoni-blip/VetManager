import os

import mysql.connector


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME", "vet_manager"),
}


def obtener_conexion():
    """Crea y devuelve una conexión a MySQL.

    Las credenciales se leen desde variables de entorno para evitar
    almacenarlas directamente en el código fuente.
    """
    if not DB_CONFIG["user"] or not DB_CONFIG["password"]:
        print(
            "Error de configuración: definí las variables "
            "DB_USER y DB_PASSWORD antes de iniciar VetManager."
        )
        return None

    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Error de conexión a MySQL: {err}")
        return None
