

import tkinter as tk
from tkinter import ttk, messagebox

# --- VENTANA PRINCIPAL (MENÚ) ---
def abrir_menu():
    global root
    root = tk.Tk()
    root.title("VetManager - Menú Principal")
    root.geometry("700x420")
    root.resizable(False, False)

    # Título superior
    lbl_titulo = tk.Label(root, text="Gestión de Turnos - Veterinaria", font=("Arial", 12, "bold"), bg="#e6f2ff", relief="solid", bd=1)
    lbl_titulo.pack(fill="x", padx=30, pady=15, ipady=6)

    # Botones principales
    btn_clientes = tk.Button(root, text="Clientes\n[ Gestionar ]", width=20, height=3, command=lambda: mensaje_en_construccion("Clientes"))
    btn_clientes.place(x=120, y=80)

    btn_mascotas = tk.Button(root, text="Mascotas\n[ Gestionar ]", width=20, height=3, command=abrir_ventana_mascota)
    btn_mascotas.place(x=380, y=80)

    btn_turnos = tk.Button(root, text="Turnos\n[ Gestionar ]", width=20, height=3, command=abrir_ventana_turnos)
    btn_turnos.place(x=120, y=160)

    btn_reporte = tk.Button(root, text="Reporte combinado\n[ Ver listado Mascota-Turno ]", width=20, height=3, command=lambda: mensaje_en_construccion("Reportes"))
    btn_reporte.place(x=380, y=160)

    # Sección de búsqueda inferior
    frame_busqueda = tk.Frame(root, bg="#f2f2f2", relief="solid", bd=1)
    frame_busqueda.place(x=120, y=250, width=460, height=100)

    lbl_busq = tk.Label(frame_busqueda, text="Buscar / Filtrar registros", bg="#f2f2f2", font=("Arial", 10))
    lbl_busq.pack(pady=5)

    entry_busq = tk.Entry(frame_busqueda, width=25)
    entry_busq.pack(side="left", padx=40)

    btn_busq = tk.Button(frame_busqueda, text="[ Buscar ]", command=lambda: messagebox.showinfo("Búsqueda", "Función de búsqueda simulada"))
    btn_busq.pack(side="left")

    root.mainloop()

def mensaje_en_construccion(modulo):
    messagebox.showinfo("Información", f"El módulo de {modulo} estará disponible próximamente.")

# --- PANTALLA: NUEVO TURNO ---
def abrir_ventana_turnos():
    ven_turno = tk.Toplevel(root)
    ven_turno.title("VetManager - Nuevo Turno")
    ven_turno.geometry("450x380")
    ven_turno.resizable(False, False)

    lbl_head = tk.Label(ven_turno, text="VetManager - Nuevo Turno", font=("Arial", 10, "bold"), bg="#34495e", fg="white", anchor="w", padx=10)
    lbl_head.pack(fill="x", ipady=5)

    # Campos del formulario
    tk.Label(ven_turno, text="Mascota:").place(x=50, y=60)
    e_mascota = tk.Entry(ven_turno, width=30)
    e_mascota.place(x=180, y=60)

    tk.Label(ven_turno, text="Fecha:").place(x=50, y=100)
    e_fecha = tk.Entry(ven_turno, width=30)
    e_fecha.place(x=180, y=100)

    tk.Label(ven_turno, text="Hora:").place(x=50, y=140)
    e_hora = tk.Entry(ven_turno, width=30)
    e_hora.place(x=180, y=140)

    tk.Label(ven_turno, text="Motivo:").place(x=50, y=180)
    e_motivo = tk.Entry(ven_turno, width=30)
    e_motivo.place(x=180, y=180)

    tk.Label(ven_turno, text="Veterinario:").place(x=50, y=220)
    e_vet = tk.Entry(ven_turno, width=30)
    e_vet.place(x=180, y=220)

    tk.Label(ven_turno, text="Estado:").place(x=50, y=260)
    e_estado = tk.Entry(ven_turno, width=30)
    e_estado.place(x=180, y=260)

    # Botones guardar y cancelar
    btn_guardar = tk.Button(ven_turno, text="[ Guardar ]", bg="#d4efdf", width=12, command=lambda: [messagebox.SUCCESS if hasattr(messagebox, 'SUCCESS') else messagebox.showinfo("Éxito", "Turno guardado con éxito"), ven_turno.destroy()])
    btn_guardar.place(x=100, y=310)

    btn_cancelar = tk.Button(ven_turno, text="[ Cancelar ]", bg="#fadbd8", width=12, command=ven_turno.destroy)
    btn_cancelar.place(x=240, y=310)


# --- PANTALLA: NUEVA MASCOTA ---
def abrir_ventana_mascota():
    ven_mascota = tk.Toplevel(root)
    ven_mascota.title("VetManager - Nueva Mascota")
    ven_mascota.geometry("400x250")
    ven_mascota.resizable(False, False)

    lbl_head = tk.Label(ven_mascota, text="VetManager - Nueva Mascota", font=("Arial", 10, "bold"), bg="#34495e", fg="white", anchor="w", padx=10)
    lbl_head.pack(fill="x", ipady=5)

    tk.Label(ven_mascota, text="Nombre:").place(x=40, y=60)
    e_nombre = tk.Entry(ven_mascota, width=25)
    e_nombre.place(x=150, y=60)

    tk.Label(ven_mascota, text="Especie:").place(x=40, y=100)
    e_especie = tk.Entry(ven_mascota, width=25)
    e_especie.place(x=150, y=100)

    tk.Label(ven_mascota, text="Cliente (dueño):").place(x=40, y=140)
    e_cliente = tk.Entry(ven_mascota, width=25)
    e_cliente.place(x=150, y=140)

    btn_guardar = tk.Button(ven_mascota, text="[ Guardar ]", bg="#d4efdf", width=10, command=ven_mascota.destroy)
    btn_guardar.place(x=90, y=190)

    btn_cancelar = tk.Button(ven_mascota, text="[ Cancelar ]", bg="#fadbd8", width=10, command=ven_mascota.destroy)
    btn_cancelar.place(x=210, y=190)

# Ejecutar programa principal
if __name__ == "__main__":
    abrir_menu()