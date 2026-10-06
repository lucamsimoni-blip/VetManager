import tkinter as tk
from tkinter import ttk, messagebox
from db import turno_dao
from views.ventana_clientes import abrir_ventana_clientes
from views.ventana_turnos import abrir_ventana_nuevo_turno


def cargar_turnero_principal(tree_turnos):
    for item in tree_turnos.get_children():
        tree_turnos.delete(item)
    registros = turno_dao.obtener_reporte_turnos()
    for fila in registros:
        tree_turnos.insert("", "end", values=fila)


def main():
    root = tk.Tk()
    root.title("VetManager - Centro de Control")
    root.geometry("950x520")
    root.resizable(False, False)

    frame_top = tk.Frame(root, bg="#2c3e50", height=60)
    frame_top.pack(fill="x", side="top")

    lbl_titulo = tk.Label(frame_top, text="VetManager 🐾", font=("Arial", 14, "bold"), bg="#2c3e50", fg="white")
    lbl_titulo.pack(side="left", padx=20, pady=10)

    # --- FUNCIONES DE ACCIÓN SOBRE TURNOS ---
    def editar_turno_seleccionado():
        item_sel = tree_turnos.selection()
        if not item_sel:
            messagebox.showwarning("Atención", "Seleccioná un turno de la lista para editar.")
            return
        datos_turno = tree_turnos.item(item_sel[0], "values")
        abrir_ventana_nuevo_turno(root, lambda: cargar_turnero_principal(tree_turnos), datos_turno)

    def eliminar_turno_seleccionado():
        item_sel = tree_turnos.selection()
        if not item_sel:
            messagebox.showwarning("Atención", "Seleccioná un turno de la lista para eliminar.")
            return

        datos_turno = tree_turnos.item(item_sel[0], "values")
        id_turno = datos_turno[0]

        if messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar el turno ID #{id_turno}?"):
            if turno_dao.eliminar_turno(id_turno):
                messagebox.showinfo("Éxito", "Turno eliminado correctamente.")
                cargar_turnero_principal(tree_turnos)
            else:
                messagebox.showerror("Error", "No se pudo eliminar el turno.")

    # --- BOTONES EN LA BARRA SUPERIOR ---
    btn_nuevo_turno = tk.Button(
        frame_top, text="+ Agendar Turno", bg="#27ae60", fg="white", font=("Arial", 9, "bold"),
        command=lambda: abrir_ventana_nuevo_turno(root, lambda: cargar_turnero_principal(tree_turnos))
    )
    btn_nuevo_turno.pack(side="right", padx=(5, 15), pady=12)

    btn_eliminar_turno = tk.Button(
        frame_top, text="🗑️ Eliminar Turno", bg="#e74c3c", fg="white", font=("Arial", 9, "bold"),
        command=eliminar_turno_seleccionado
    )
    btn_eliminar_turno.pack(side="right", padx=5, pady=12)

    btn_editar_turno = tk.Button(
        frame_top, text="✏️ Editar Turno", bg="#f39c12", fg="white", font=("Arial", 9, "bold"),
        command=editar_turno_seleccionado
    )
    btn_editar_turno.pack(side="right", padx=5, pady=12)

    btn_gest_clientes = tk.Button(
        frame_top, text="👥 Gestor Clientes / Mascotas", bg="#2980b9", fg="white", font=("Arial", 9, "bold"),
        command=lambda: abrir_ventana_clientes(root)
    )
    btn_gest_clientes.pack(side="right", padx=5, pady=12)

    # --- TABLA CENTRAL ---
    frame_center = tk.LabelFrame(root, text=" Turnero General / Estado de Atenciones ", font=("Arial", 10, "bold"), padx=10, pady=10)
    frame_center.pack(fill="both", expand=True, padx=20, pady=15)

    columnas = ("id", "fecha", "hora", "mascota", "cliente", "veterinario", "motivo", "estado")
    tree_turnos = ttk.Treeview(frame_center, columns=columnas, show="headings", height=12)

    tree_turnos.heading("id", text="ID")
    tree_turnos.heading("fecha", text="Fecha")
    tree_turnos.heading("hora", text="Hora")
    tree_turnos.heading("mascota", text="Mascota")
    tree_turnos.heading("cliente", text="Cliente (Dueño)")
    tree_turnos.heading("veterinario", text="Veterinario")
    tree_turnos.heading("motivo", text="Motivo Consulta")
    tree_turnos.heading("estado", text="Estado")

    tree_turnos.column("id", width=30, anchor="center")
    tree_turnos.column("fecha", width=80, anchor="center")
    tree_turnos.column("hora", width=60, anchor="center")
    tree_turnos.column("mascota", width=100)
    tree_turnos.column("cliente", width=140)
    tree_turnos.column("veterinario", width=130)
    tree_turnos.column("motivo", width=180)
    tree_turnos.column("estado", width=90, anchor="center")

    tree_turnos.pack(fill="both", expand=True)

    # Atajo: hacer doble clic en una fila abre directamente la ventana de edición
    tree_turnos.bind("<Double-1>", lambda event: editar_turno_seleccionado())

    cargar_turnero_principal(tree_turnos)

    root.mainloop()

if __name__ == "__main__":
    main()
    
