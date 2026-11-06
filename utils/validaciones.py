import re
from datetime import datetime, date


def validar_campo_vacio(texto, nombre_campo):
    if not texto or not texto.strip():
        return False, f"El campo '{nombre_campo}' no puede estar vacío."
    return True, ""


def validar_solo_fecha(texto):
    """Permite ingresar únicamente dígitos y guiones (-) mientras se escribe."""
    if texto == "":
        return True
    return bool(re.match(r'^[0-9\-]*$', texto))


def validar_solo_hora(texto):
    """Permite ingresar únicamente dígitos y dos puntos (:) mientras se escribe."""
    if texto == "":
        return True
    return bool(re.match(r'^[0-9:]*$', texto))


def validar_fecha(fecha_texto):
    """Comprueba que la fecha exista y que no sea anterior al día actual."""
    try:
        fecha = datetime.strptime(fecha_texto, "%Y-%m-%d").date()
    except ValueError:
        return False, "La fecha debe ser válida y tener el formato AAAA-MM-DD."

    if fecha.strftime("%Y-%m-%d") != fecha_texto:
        return False, "La fecha debe tener exactamente el formato AAAA-MM-DD."

    if fecha < date.today():
        return False, "No se pueden agendar turnos en fechas anteriores a hoy."

    return True, ""


def validar_hora(hora_texto):
    """Comprueba el formato y que la hora esté dentro del horario de atención."""
    try:
        hora = datetime.strptime(hora_texto, "%H:%M").time()
    except ValueError:
        return False, "La hora debe ser válida y tener el formato HH:MM."

    if hora.strftime("%H:%M") != hora_texto:
        return False, "La hora debe tener exactamente el formato HH:MM."

    hora_minima = datetime.strptime("08:00", "%H:%M").time()
    hora_maxima = datetime.strptime("18:30", "%H:%M").time()

    if not hora_minima <= hora <= hora_maxima:
        return False, "El horario de atención es de 08:00 a 18:30."

    if hora.minute not in (0, 30):
        return False, "Los turnos deben comenzar en intervalos de 30 minutos."

    return True, ""


def validar_telefono(telefono):
    if not telefono.isdigit() or len(telefono) < 7:
        return False, "El teléfono debe contener solo números (mínimo 7 dígitos)."
    return True, ""


def validar_email(email):
    if not email.strip():
        return True, ""  # Si es opcional
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(patron, email.strip()):
        return False, "El formato del e-mail no es válido (ejemplo@dominio.com)."
    return True, ""
