import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from db import turno_dao, mascota_dao
from utils import validaciones


def generar_opciones_fechas(dias_adelante=30):
    hoy = datetime.now()
    fechas = []
    for i in range(dias_adelante):
        fecha = hoy + timedelta(days=i)
        fechas.append(fecha.strftime("%Y-%m-%d"))
    return fechas


def generar_opciones_horas(inicio=8, fin=19, intervalo_min=30):
    horas = []
    for h in range(inicio, fin):
        for m in (0, intervalo_min):
            horas.append(f"{h:02d}:{m:02d}")
    return horas


def abrir_ventana_nuevo_turno(parent, callback_recargar, datos_turno=None):
    es_edicion = datos_turno is not None
    ven_t = tk.Toplevel(parent)
    ven_t.title("VetManager - Editar Turno" if es_edicion else "VetManager - Agendar Nuevo Turno")
    ven_t.geometry("420x350")
    ven_t.resizable(False, False)

    mascotas_db = mascota_dao.obtener_mascotas()
    vets_db = turno_dao.obtener_veterinarios()

    mapa_mascotas = {f"{m[1]} (ID: {m[0]})": m[0] for m in mascotas_db}
    mapa_vets = {f"{v[1]} {v[2]} (ID: {v[0]})": v[0] for v in vets_db}

    mapa_mascotas_inv = {m[0]: f"{m[1]} (ID: {m[0]})" for m in mascotas_db}
    mapa_vets_inv = {v[0]: f"{v[1]} {v[2]} (ID: {v[0]})" for v in vets_db}

    opciones_fechas = generar_opciones_fechas(dias_adelante=30)
    opciones_horas = generar_opciones_horas(inicio=8, fin=19, intervalo_min=30)

    tk.Label(ven_t, text="Mascota:").place(x=40, y=40)
    cb_masc = ttk.Combobox(ven_t, values=list(mapa_mascotas.keys()), width=27, state="readonly")
    cb_masc.place(x=160, y=40)

    tk.Label(ven_t, text="Fecha:").place(x=40, y=80)
    cb_fec = ttk.Combobox(ven_t, values=opciones_fechas, width=27)
    cb_fec.place(x=160, y=80)
    if opciones_fechas and not es_edicion:
        cb_fec.set(opciones_fechas[0])

    tk.Label(ven_t, text="Hora:").place(x=40, y=120)
    cb_hor = ttk.Combobox(ven_t, values=opciones_horas, width=27)
    cb_hor.place(x=160, y=120)
    if opciones_horas and not es_edicion:
        cb_hor.set("09:00")

    tk.Label(ven_t, text="Motivo:").place(x=40, y=160)
    e_mot = tk.Entry(ven_t, width=30)
    e_mot.place(x=160, y=160)

    tk.Label(ven_t, text="Veterinario:").place(x=40, y=200)
    cb_vet = ttk.Combobox(ven_t, values=list(mapa_vets.keys()), width=27, state="readonly")
    cb_vet.place(x=160, y=200)

    tk.Label(ven_t, text="Estado:").place(x=40, y=240)
    cb_est = ttk.Combobox(
        ven_t,
        values=["Pendiente", "Atendido", "Cancelado"],
        width=27,
        state="readonly"
    )
    cb_est.set("Pendiente")
    cb_est.place(x=160, y=240)

    if es_edicion:
        cb_fec.set(str(datos_turno[1]))

        hora_str = str(datos_turno[2])
        if len(hora_str.split(":")) == 3:
            hora_str = ":".join(hora_str.split(":")[:2])
        cb_hor.set(hora_str)

        e_mot.insert(0, datos_turno[6])
        cb_est.set(datos_turno[7])

        for key in mapa_mascotas:
            if datos_turno[3] in key:
                cb_masc.set(key)
                break

        for key in mapa_vets:
            if datos_turno[5] in key:
                cb_vet.set(key)
                break

    def guardar():
        fecha = cb_fec.get().strip()
        hora = cb_hor.get().strip()
        motivo = e_mot.get().strip()
        estado = cb_est.get()
        masc_sel = cb_masc.get()
        vet_sel = cb_vet.get()

        if not motivo:
            messagebox.showwarning("Validación", "El campo 'Motivo' no puede estar vacío.")
            return

        if not masc_sel or not vet_sel or not fecha or not hora:
            messagebox.showwarning("Validación", "Debe completar todos los campos del formulario.")
            return

        fecha_valida, mensaje_fecha = validaciones.validar_fecha(fecha)
        if not fecha_valida:
            messagebox.showwarning("Validación de fecha", mensaje_fecha)
            return

        hora_valida, mensaje_hora = validaciones.validar_hora(hora)
        if not hora_valida:
            messagebox.showwarning("Validación de hora", mensaje_hora)
            return

        id_mascota = mapa_mascotas[masc_sel]
        id_vet = mapa_vets[vet_sel]
        id_turno = datos_turno[0] if es_edicion else None

        disponible, mensaje = turno_dao.verificar_disponibilidad_turno(
            fecha,
            hora,
            id_vet,
            id_mascota,
            id_turno=id_turno,
            estado=estado
        )
        if not disponible:
            messagebox.showwarning("Horario no disponible", mensaje)
            return

        if es_edicion:
            exito = turno_dao.actualizar_turno(
                id_turno, fecha, hora, motivo, estado, id_vet, id_mascota
            )
            msg_ok = "Turno actualizado correctamente."
        else:
            exito = turno_dao.insertar_turno(
                fecha, hora, motivo, estado, id_vet, id_mascota
            )
            msg_ok = "Turno agendado con éxito."

        if exito:
            messagebox.showinfo("Éxito", msg_ok)
            ven_t.destroy()
            callback_recargar()
        else:
            messagebox.showerror(
                "Error",
                "No se pudo guardar el turno. Es posible que otro turno haya ocupado ese horario."
            )

    btn = tk.Button(
        ven_t,
        text="Actualizar Turno" if es_edicion else "Guardar Turno",
        bg="#27ae60",
        fg="white",
        font=("Arial", 9, "bold"),
        command=guardar
    )
    btn.place(x=150, y=290)
