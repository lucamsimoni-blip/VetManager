import mysql.connector
from db.conexion import obtener_conexion

def insertar_turno(fecha, hora, motivo, estado, id_veterinario, id_mascota):
    conn = obtener_conexion()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO turno (fecha, hora, motivo, estado, id_veterinario, id_mascota)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (fecha, hora, motivo, estado, id_veterinario, id_mascota))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al insertar turno: {err}")
        return False

def obtener_veterinarios():
    conn = obtener_conexion()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_veterinario, nombre, apellido FROM veterinario")
        vets = cursor.fetchall()
        cursor.close()
        conn.close()
        return vets
    except mysql.connector.Error as err:
        print(f"Error al obtener veterinarios: {err}")
        return []

def obtener_reporte_turnos():
    conn = obtener_conexion()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        query = """
            SELECT
            t.id_turno,
                t.fecha,
                TIME_FORMAT(t.hora, '%H:%i') AS hora,  
                m.nombre AS mascota,
                CONCAT(c.nombre, ' ', c.apellido) AS cliente,
                CONCAT(v.nombre, ' ', v.apellido) AS veterinario,
                t.motivo,
                t.estado
            FROM turno t
            JOIN mascota m ON t.id_mascota = m.id_mascota
            JOIN cliente c ON m.id_cliente = c.id_cliente
            JOIN veterinario v ON t.id_veterinario = v.id_veterinario
        """
        cursor.execute(query)
        reporte = cursor.fetchall()
        cursor.close()
        conn.close()
        return reporte
    except mysql.connector.Error as err:
        print(f"Error al obtener el reporte de turnos: {err}")
        return []



def actualizar_turno(id_turno, fecha, hora, motivo, estado, id_veterinario, id_mascota):
    conn = obtener_conexion()
    if not conn: return False
    try:
        cursor = conn.cursor()
        sql = """
            UPDATE turno 
            SET fecha=%s, hora=%s, motivo=%s, estado=%s, id_veterinario=%s, id_mascota=%s 
            WHERE id_turno=%s
        """
        cursor.execute(sql, (fecha, hora, motivo, estado, id_veterinario, id_mascota, id_turno))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al actualizar turno: {err}")
        return False

def eliminar_turno(id_turno):
    conn = obtener_conexion()
    if not conn: return False
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM turno WHERE id_turno = %s"
        cursor.execute(sql, (id_turno,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error al eliminar turno: {err}")
        return False