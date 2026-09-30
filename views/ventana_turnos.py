import tkinter as tk
from tkinter import ttk, messagebox
from db import turno_dao, mascota_dao
from utils import validaciones

def abrir_ventana_nuevo_turno(parent, callback_recargar):
    ven_t = tk.Toplevel(parent)
    ven_t.title("VetManager - Agendar Nuevo Turno")
    ven_t.geometry("420x350")

    mascotas_db = mascota_dao.obtener_mascotas()
    vets_db = turno_dao.obtener_veterinarios()

    mapa_mascotas = {f"{m[1]} (ID: {m[0]})": m[0] for m in mascotas_db}
    mapa_vets = {f"{v[1]} {v[2]} (ID: {v[0]})": v[0] for v in vets_db}

    tk.Label(ven_t, text="Mascota:").place(x=40, y=40)
    cb_masc = ttk.Combobox(ven_t, values=list(mapa_mascotas.keys()), width=27, state="readonly")
    cb_masc.place(x=160, y=40)

    tk.Label(ven_t, text="Fecha (AAAA-MM-DD):").place(x=40, y=80)
    e_fec = tk.Entry(ven_t, width=30); e_fec.place(x=160, y=80)

    tk.Label(ven_t, text="Hora (HH:MM):").place(x=40, y=120)
    e_hor = tk.Entry(ven_t, width=30); e_hor.place(x=160, y=120)

    tk.Label(ven_t, text="Motivo:").place(x=40, y=160)
    e_mot = tk.Entry(ven_t, width=30); e_mot.place(x=160, y=160)

    tk.Label(ven_t, text="Veterinario:").place(x=40, y=200)
    cb_vet = ttk.Combobox(ven_t, values=list(mapa_vets.keys()), width=27, state="readonly")
    cb_vet.place(x=160, y=200)

    tk.Label(ven_t, text="Estado:").place(x=40, y=240)
    cb_est = ttk.Combobox(ven_t, values=["Pendiente", "Atendido", "Cancelado"], width=27, state="readonly")
    cb_est.set("Pendiente")
    cb_est.place(x=160, y=240)

    def guardar():
        fecha, hora, motivo = e_fec.get().strip(), e_hor.get().strip(), e_mot.get().strip()
        estado, masc_sel, vet_sel = cb_est.get(), cb_masc.get(), cb_vet.get()

        for val, campo in [(fecha, "Fecha"), (hora, "Hora"), (motivo, "Motivo")]:
            ok, msg = validaciones.validar_campo_vacio(val, campo)
            if not ok: messagebox.showwarning("Validación", msg); return

        if not masc_sel or not vet_sel:
            messagebox.showwarning("Validación", "Debe seleccionar una mascota y un veterinario.")
            return

        id_mascota = mapa_mascotas[masc_sel]
        id_vet = mapa_vets[vet_sel]

        if turno_dao.insertar_turno(fecha, hora, motivo, estado, id_vet, id_mascota):
            messagebox.showinfo("Éxito", "Turno agendado con éxito.")
            ven_t.destroy()
            callback_recargar()
        else:
            messagebox.showerror("Error", "No se pudo agendar el turno.")

    btn = tk.Button(ven_t, text="Guardar Turno", bg="#27ae60", fg="white", font=("Arial", 9, "bold"), command=guardar)
    btn.place(x=150, y=290)