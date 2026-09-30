import mysql.connector
from db.conexion import obtener_conexion

def obtener_especies():
    conn = obtener_conexion()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_especie, nombre FROM especie ORDER BY nombre ASC")
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return filas
    except mysql.connector.Error as err:
        print(f"Error al obtener especies: {err}")
        return []
    
