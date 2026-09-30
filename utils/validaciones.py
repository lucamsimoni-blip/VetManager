import re

def validar_campo_vacio(texto, nombre_campo):
    if not texto or not texto.strip():
        return False, f"El campo '{nombre_campo}' no puede estar vacío."
    return True, ""

def validar_telefono(telefono):
    if not telefono.isdigit() or len(telefono) < 7:
        return False, "El teléfono debe contener solo números (mínimo 7 dígitos)."
    return True, ""

def validar_email(email):
    if not email.strip():
        return True, "" # Si es opcional
    patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(patron, email.strip()):
        return False, "El formato del e-mail no es válido (ejemplo@dominio.com)."
    return True, ""