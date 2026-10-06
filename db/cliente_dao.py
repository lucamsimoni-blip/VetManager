import mysql.connector
from db.conexion import obtener_conexion

def insertar_cliente(nombre, apellido, telefono, email="", direccion=""):
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO cliente (nombre, apellido, telefono, email, direccion) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nombre, apellido, telefono, email, direccion))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al insertar cliente: {err}")
        return False

def obtener_clientes():
    conn = obtener_conexion()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nombre, apellido, telefono, email, direccion FROM cliente ORDER BY id_cliente DESC")
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return filas
    except mysql.connector.Error as err:
        print(f"Error al obtener clientes: {err}")
        return []

def obtener_mascotas_por_cliente(id_cliente):
    conn = obtener_conexion()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        sql = """
            SELECT m.id_mascota, m.nombre, e.nombre AS especie
            FROM mascota m
            INNER JOIN especie e ON m.id_especie = e.id_especie
            WHERE m.id_cliente = %s
        """
        cursor.execute(sql, (id_cliente,))
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return filas
    except mysql.connector.Error as err:
        print(f"Error al obtener mascotas del cliente: {err}")
        return []
    
    
def actualizar_cliente(id_cliente, nombre, apellido, telefono, email):
    conn = obtener_conexion()
    if not conn: return False
    try:
        cursor = conn.cursor()
        sql = "UPDATE cliente SET nombre=%s, apellido=%s, telefono=%s, email=%s WHERE id_cliente=%s"
        cursor.execute(sql, (nombre, apellido, telefono, email, id_cliente))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al actualizar cliente: {err}")
        return False

def eliminar_cliente(id_cliente):
    conn = obtener_conexion()
    if not conn: return False
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM cliente WHERE id_cliente = %s"
        cursor.execute(sql, (id_cliente,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al eliminar cliente: {err}")
        return False