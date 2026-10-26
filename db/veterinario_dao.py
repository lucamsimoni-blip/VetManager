import mysql.connector
from db.conexion import obtener_conexion

def insertar_veterinario(nombre, apellido, especialidad):
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = "INSERT INTO veterinario (nombre, apellido, especialidad) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, apellido, especialidad))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al insertar veterinario: {err}")
        return False

def obtener_veterinarios():
    conn = obtener_conexion()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        query = "SELECT id_veterinario, nombre, apellido, especialidad FROM veterinario"
        cursor.execute(query)
        filas = cursor.fetchall()
        cursor.close()
        conn.close()
        return filas
    except mysql.connector.Error as err:
        print(f"Error al obtener veterinarios: {err}")
        return []

def actualizar_veterinario(id_veterinario, nombre, apellido, especialidad):
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = "UPDATE veterinario SET nombre = %s, apellido = %s, especialidad = %s WHERE id_veterinario = %s"
        cursor.execute(query, (nombre, apellido, especialidad, id_veterinario))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al actualizar veterinario: {err}")
        return False

def eliminar_veterinario(id_veterinario):
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = "DELETE FROM veterinario WHERE id_veterinario = %s"
        cursor.execute(query, (id_veterinario,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al eliminar veterinario: {err}")
        return False