import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from db import turno_dao, mascota_dao


def generar_opciones_fechas(dias_adelante=30):
    """Genera una lista de fechas desde hoy hacia el futuro en formato AAAA-MM-DD."""
    hoy = datetime.now()
    fechas = []
    for i in range(dias_adelante):
        fecha = hoy + timedelta(days=i)
        fechas.append(fecha.strftime("%Y-%m-%d"))
    return fechas


def generar_opciones_horas(inicio=8, fin=19, intervalo_min=30):
    """Genera lista de horarios desde 'inicio' hs hasta 'fin' hs cada 'intervalo_min' minutos."""
    horas = []
    for h in range(inicio, fin):
        for m in (0, intervalo_min):
            horas.append(f"{h:02d}:{m:02d}")
    return horas


def abrir_ventana_nuevo_turno(parent, callback_recargar):
    ven_t = tk.Toplevel(parent)
    ven_t.title("VetManager - Agendar Nuevo Turno")
    ven_t.geometry("420x350")
    ven_t.resizable(False, False)

    # 1. Cargar datos de la BD
    mascotas_db = mascota_dao.obtener_mascotas()
    vets_db = turno_dao.obtener_veterinarios()

    mapa_mascotas = {f"{m[1]} (ID: {m[0]})": m[0] for m in mascotas_db}
    mapa_vets = {f"{v[1]} {v[2]} (ID: {v[0]})": v[0] for v in vets_db}

    # 2. Generar listas de opciones para los desplegables
    opciones_fechas = generar_opciones_fechas(dias_adelante=30)
    opciones_horas = generar_opciones_horas(inicio=8, fin=19, intervalo_min=30)

    # --- CAMPOS DE LA INTERFAZ ---
    # Mascota
    tk.Label(ven_t, text="Mascota:").place(x=40, y=40)
    cb_masc = ttk.Combobox(ven_t, values=list(mapa_mascotas.keys()), width=27, state="readonly")
    cb_masc.place(x=160, y=40)

    # Fecha (Desplegable)
    tk.Label(ven_t, text="Fecha:").place(x=40, y=80)
    cb_fec = ttk.Combobox(ven_t, values=opciones_fechas, width=27, state="readonly")
    cb_fec.place(x=160, y=80)
    if opciones_fechas:
        cb_fec.set(opciones_fechas[0])  # Selecciona la fecha de HOY por defecto

    # Hora (Desplegable)
    tk.Label(ven_t, text="Hora:").place(x=40, y=120)
    cb_hor = ttk.Combobox(ven_t, values=opciones_horas, width=27, state="readonly")
    cb_hor.place(x=160, y=120)
    if opciones_horas:
        cb_hor.set("09:00")  # Hora sugerida por defecto

    # Motivo (Sigue siendo Entry libre)
    tk.Label(ven_t, text="Motivo:").place(x=40, y=160)
    e_mot = tk.Entry(ven_t, width=30)
    e_mot.place(x=160, y=160)

    # Veterinario
    tk.Label(ven_t, text="Veterinario:").place(x=40, y=200)
    cb_vet = ttk.Combobox(ven_t, values=list(mapa_vets.keys()), width=27, state="readonly")
    cb_vet.place(x=160, y=200)

    # Estado
    tk.Label(ven_t, text="Estado:").place(x=40, y=240)
    cb_est = ttk.Combobox(ven_t, values=["Pendiente", "Atendido", "Cancelado"], width=27, state="readonly")
    cb_est.set("Pendiente")
    cb_est.place(x=160, y=240)

    def guardar():
        fecha = cb_fec.get()
        hora = cb_hor.get()
        motivo = e_mot.get().strip()
        estado = cb_est.get()
        masc_sel = cb_masc.get()
        vet_sel = cb_vet.get()

        # Validación 1: Verificar motivo
        if not motivo:
            messagebox.showwarning("Validación", "El campo 'Motivo' no puede estar vacío.")
            return

        # Validación 2: Selección de Comboboxes
        if not masc_sel or not vet_sel or not fecha or not hora:
            messagebox.showwarning("Validación", "Debe completar todos los campos del formulario.")
            return

        # Mapeo de IDs
        id_mascota = mapa_mascotas[masc_sel]
        id_vet = mapa_vets[vet_sel]

        # Inserción en la BD
        if turno_dao.insertar_turno(fecha, hora, motivo, estado, id_vet, id_mascota):
            messagebox.showinfo("Éxito", "Turno agendado con éxito.")
            ven_t.destroy()
            callback_recargar()
        else:
            messagebox.showerror("Error", "No se pudo agendar el turno.")

    btn = tk.Button(
        ven_t, 
        text="Guardar Turno", 
        bg="#27ae60", 
        fg="white", 
        font=("Arial", 9, "bold"), 
        command=guardar
    )
    btn.place(x=150, y=290)