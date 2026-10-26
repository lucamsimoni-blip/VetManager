import tkinter as tk
from tkinter import ttk, messagebox
from db import veterinario_dao

def abrir_ventana_veterinarios(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("VetManager - Gestor de Veterinarios")
    ventana.geometry("600x400")
    ventana.resizable(False, False)
    ventana.grab_set()

    lbl_titulo = tk.Label(ventana, text="Gestión de Profesionales", font=("Arial", 12, "bold"), fg="#2c3e50")
    lbl_titulo.pack(pady=10)

    # Frame para formulario superior
    frame_form = tk.LabelFrame(ventana, text=" Registrar / Editar Veterinario ", font=("Arial", 9, "bold"), padx=10, pady=10)
    frame_form.pack(fill="x", padx=15, pady=5)

    tk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
    entry_nombre = tk.Entry(frame_form, width=20)
    entry_nombre.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(frame_form, text="Apellido:").grid(row=0, column=2, sticky="e", padx=5, pady=2)
    entry_apellido = tk.Entry(frame_form, width=20)
    entry_apellido.grid(row=0, column=3, padx=5, pady=2)

    tk.Label(frame_form, text="Especialidad:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
    entry_especialidad = tk.Entry(frame_form, width=20)
    entry_especialidad.grid(row=1, column=1, padx=5, pady=2)

    var_id_sel = tk.StringVar(value="")

    def limpiar_form():
        var_id_sel.set("")
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_especialidad.delete(0, tk.END)
        btn_guardar.config(text="Guardar", bg="#27ae60")

    def guardar_vet():
        nom = entry_nombre.get().strip()
        ape = entry_apellido.get().strip()
        esp = entry_especialidad.get().strip()
        id_vet = var_id_sel.get()

        if not nom or not ape or not esp:
            messagebox.showwarning("Atención", "Todos los campos son obligatorios.", parent=ventana)
            return

        if id_vet:
            # Edición
            if veterinario_dao.actualizar_veterinario(id_vet, nom, ape, esp):
                messagebox.showinfo("Éxito", "Veterinario actualizado correctamente.", parent=ventana)
                limpiar_form()
                cargar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo actualizar el registro.", parent=ventana)
        else:
            # Alta
            if veterinario_dao.insertar_veterinario(nom, ape, esp):
                messagebox.showinfo("Éxito", "Veterinario registrado correctamente.", parent=ventana)
                limpiar_form()
                cargar_tabla()
            else:
                messagebox.showerror("Error", "No se pudo registrar el veterinario.", parent=ventana)

    btn_guardar = tk.Button(frame_form, text="Guardar", bg="#27ae60", fg="white", font=("Arial", 9, "bold"), command=guardar_vet)
    btn_guardar.grid(row=1, column=2, padx=5, pady=2)

    btn_cancelar = tk.Button(frame_form, text="Limpiar", bg="#7f8c8d", fg="white", font=("Arial", 9), command=limpiar_form)
    btn_cancelar.grid(row=1, column=3, padx=5, pady=2)

    # Tabla
    columnas = ("id", "nombre", "apellido", "especialidad")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings", height=8)
    tree.heading("id", text="ID")
    tree.heading("nombre", text="Nombre")
    tree.heading("apellido", text="Apellido")
    tree.heading("especialidad", text="Especialidad")

    tree.column("id", width=40, anchor="center")
    tree.column("nombre", width=140)
    tree.column("apellido", width=140)
    tree.column("especialidad", width=180)
    tree.pack(fill="both", expand=True, padx=15, pady=5)

    def cargar_tabla():
        for item in tree.get_children():
            tree.delete(item)
        for fila in veterinario_dao.obtener_veterinarios():
            tree.insert("", "end", values=fila)

    def seleccionar_de_tabla(event):
        item_sel = tree.selection()
        if not item_sel:
            return
        datos = tree.item(item_sel[0], "values")
        var_id_sel.set(datos[0])
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, datos[1])
        entry_apellido.delete(0, tk.END)
        entry_apellido.insert(0, datos[2])
        entry_especialidad.delete(0, tk.END)
        entry_especialidad.insert(0, datos[3])
        btn_guardar.config(text="Actualizar", bg="#f39c12")

    tree.bind("<Double-1>", seleccionar_de_tabla)

    def eliminar_vet():
        item_sel = tree.selection()
        if not item_sel:
            messagebox.showwarning("Atención", "Seleccioná un veterinario de la lista para eliminar.", parent=ventana)
            return
        datos = tree.item(item_sel[0], "values")
        id_vet = datos[0]
        nom_vet = f"{datos[1]} {datos[2]}"

        if messagebox.askyesno("Confirmar", f"¿Eliminar al Dr./Dra. {nom_vet}?", parent=ventana):
            if veterinario_dao.eliminar_veterinario(id_vet):
                messagebox.showinfo("Éxito", "Veterinario eliminado correctamente.", parent=ventana)
                limpiar_form()
                cargar_tabla()
            else:
                messagebox.showerror("Error", "No se puede eliminar al profesional porque posee turnos asociados (ON DELETE RESTRICT).", parent=ventana)

    frame_bot = tk.Frame(ventana)
    frame_bot.pack(fill="x", padx=15, pady=8)

    btn_eliminar = tk.Button(frame_bot, text="🗑️ Eliminar Seleccionado", bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), command=eliminar_vet)
    btn_eliminar.pack(side="right")

    cargar_tabla()