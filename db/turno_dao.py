import mysql.connector
from db.conexion import obtener_conexion


def _cerrar_recursos(cursor, conn):
    """Cierra el cursor y la conexión aunque ocurra un error."""
    if cursor is not None:
        cursor.close()
    if conn is not None and conn.is_connected():
        conn.close()


def verificar_disponibilidad_turno(fecha, hora, id_veterinario, id_mascota,
                                    id_turno=None, estado="Pendiente"):
    """
    Comprueba que no exista otro turno activo para el mismo veterinario
    o la misma mascota en la misma fecha y hora.
    Los turnos cancelados no bloquean el horario.
    """
    if estado == "Cancelado":
        return True, ""

    conn = obtener_conexion()
    if not conn:
        return False, "No se pudo conectar con la base de datos."

    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            SELECT id_veterinario, id_mascota
            FROM turno
            WHERE fecha = %s
              AND hora = %s
              AND estado <> 'Cancelado'
        """
        parametros = [fecha, hora]

        if id_turno is not None:
            query += " AND id_turno <> %s"
            parametros.append(id_turno)

        cursor.execute(query, tuple(parametros))
        turnos = cursor.fetchall()

        for vet_existente, mascota_existente in turnos:
            if vet_existente == id_veterinario:
                return False, "El veterinario seleccionado ya tiene un turno activo en esa fecha y hora."
            if mascota_existente == id_mascota:
                return False, "La mascota seleccionada ya tiene un turno activo en esa fecha y hora."

        return True, ""
    except mysql.connector.Error as err:
        print(f"Error al verificar disponibilidad del turno: {err}")
        return False, "No se pudo verificar la disponibilidad del horario."
    finally:
        _cerrar_recursos(cursor, conn)


def insertar_turno(fecha, hora, motivo, estado, id_veterinario, id_mascota):
    conn = obtener_conexion()
    if not conn:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO turno (fecha, hora, motivo, estado, id_veterinario, id_mascota)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (fecha, hora, motivo, estado, id_veterinario, id_mascota))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error al insertar turno: {err}")
        return False
    finally:
        _cerrar_recursos(cursor, conn)


def obtener_veterinarios():
    conn = obtener_conexion()
    if not conn:
        return []

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_veterinario, nombre, apellido FROM veterinario")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error al obtener veterinarios: {err}")
        return []
    finally:
        _cerrar_recursos(cursor, conn)


def obtener_reporte_turnos():
    conn = obtener_conexion()
    if not conn:
        return []

    cursor = None
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
            ORDER BY t.fecha ASC, t.hora ASC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error al obtener el reporte de turnos: {err}")
        return []
    finally:
        _cerrar_recursos(cursor, conn)


def actualizar_turno(id_turno, fecha, hora, motivo, estado, id_veterinario, id_mascota):
    conn = obtener_conexion()
    if not conn:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        sql = """
            UPDATE turno
            SET fecha=%s, hora=%s, motivo=%s, estado=%s,
                id_veterinario=%s, id_mascota=%s
            WHERE id_turno=%s
        """
        cursor.execute(
            sql,
            (fecha, hora, motivo, estado, id_veterinario, id_mascota, id_turno)
        )
        conn.commit()
        return True
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error al actualizar turno: {err}")
        return False
    finally:
        _cerrar_recursos(cursor, conn)


def eliminar_turno(id_turno):
    conn = obtener_conexion()
    if not conn:
        return False

    cursor = None
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM turno WHERE id_turno = %s"
        cursor.execute(sql, (id_turno,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error al eliminar turno: {err}")
        return False
    finally:
        _cerrar_recursos(cursor, conn)


def buscar_turnos(criterio):
    conn = obtener_conexion()
    if not conn:
        return []

    cursor = None
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
            WHERE m.nombre LIKE %s
               OR c.nombre LIKE %s
               OR c.apellido LIKE %s
               OR v.nombre LIKE %s
               OR t.estado LIKE %s
            ORDER BY t.fecha ASC, t.hora ASC
        """
        valor = f"%{criterio}%"
        cursor.execute(query, (valor, valor, valor, valor, valor))
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error al buscar turnos: {err}")
        return []
    finally:
        _cerrar_recursos(cursor, conn)
