import mysql.connector
from db.conexion import obtener_conexion

def insertar_mascota(nombre, id_especie, id_cliente):
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO mascota (nombre, id_especie, id_cliente) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, id_especie, id_cliente))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al insertar mascota: {err}")
        return False

def obtener_mascotas():
    conn = obtener_conexion()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        sql = """
            SELECT m.id_mascota, m.nombre, e.nombre AS especie, m.id_cliente 
            FROM mascota m
            INNER JOIN especie e ON m.id_especie = e.id_especie
        """
        cursor.execute(sql)
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return filas
    except mysql.connector.Error as err:
        print(f"Error al obtener mascotas: {err}")
        return []
    
def obtener_especies():
    conn = obtener_conexion()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        sql = "SELECT id_especie, nombre FROM especie"
        cursor.execute(sql)
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return filas
    except mysql.connector.Error as err:
        print(f"Error al obtener especies: {err}")
        return []
    
    
def actualizar_mascota(id_mascota, nombre, id_especie):
    conn = obtener_conexion()
    if not conn: return False
    try:
        cursor = conn.cursor()
        sql = "UPDATE mascota SET nombre=%s, id_especie=%s WHERE id_mascota=%s"
        cursor.execute(sql, (nombre, id_especie, id_mascota))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al actualizar mascota: {err}")
        return False

def eliminar_mascota(id_mascota):
    conn = obtener_conexion()
    if not conn: return False
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM mascota WHERE id_mascota = %s"
        cursor.execute(sql, (id_mascota,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al eliminar mascota: {err}")
        return False