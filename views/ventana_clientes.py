import tkinter as tk
from tkinter import ttk, messagebox
from db import cliente_dao, mascota_dao, especie_dao
from utils import validaciones


def cargar_tabla_clientes(tree_clientes):
    for item in tree_clientes.get_children():
        tree_clientes.delete(item)
    for c in cliente_dao.obtener_clientes():
        tree_clientes.insert("", "end", values=c)


def cargar_tabla_mascotas_cliente(tree_mascotas, id_cliente):
    for item in tree_mascotas.get_children():
        tree_mascotas.delete(item)
    for m in cliente_dao.obtener_mascotas_por_cliente(id_cliente):
        tree_mascotas.insert("", "end", values=m)


def abrir_ventana_clientes(parent):
    ven_cli = tk.Toplevel(parent)
    ven_cli.title("VetManager - Gestor de Clientes y Mascotas")
    ven_cli.geometry("820x520")
    ven_cli.resizable(False, False)

    f_top = tk.Frame(ven_cli)
    f_top.pack(fill="x", padx=15, pady=10)

    # --- BOTONES SUPERIORES CLIENTE ---
    btn_add_cli = tk.Button(
        f_top,
        text="+ Nuevo Cliente",
        bg="#27ae60",
        fg="white",
        font=("Arial", 9, "bold"),
        command=lambda: abrir_form_cliente(ven_cli, tree_cli)
    )
    btn_add_cli.pack(side="left", padx=(0, 5))

    btn_edit_cli = tk.Button(
        f_top,
        text="✏️️ Editar Cliente",
        bg="#f39c12",
        fg="white",
        font=("Arial", 9, "bold"),
        state="disabled"
    )
    btn_edit_cli.pack(side="left", padx=5)

    btn_del_cli = tk.Button(
        f_top,
        text="🗑️ Eliminar Cliente",
        bg="#e74c3c",
        fg="white",
        font=("Arial", 9, "bold"),
        state="disabled"
    )
    btn_del_cli.pack(side="left", padx=5)

    lbl_info = tk.Label(
        f_top,
        text="💡 Seleccioná un cliente para ver o gestionar sus mascotas",
        font=("Arial", 9, "italic"),
        fg="#7f8c8d"
    )
    lbl_info.pack(side="right")

    # --- TABLA CLIENTES ---
    tree_cli = ttk.Treeview(ven_cli, columns=("id", "nom", "ape", "tel", "mail", "dir"), show="headings", height=7)
    tree_cli.heading("id", text="ID")
    tree_cli.heading("nom", text="Nombre")
    tree_cli.heading("ape", text="Apellido")
    tree_cli.heading("tel", text="Teléfono")
    tree_cli.heading("mail", text="Email")
    tree_cli.heading("dir", text="Dirección")

    tree_cli.column("id", width=30)
    tree_cli.column("nom", width=100)
    tree_cli.column("ape", width=100)
    tree_cli.column("tel", width=100)
    tree_cli.column("mail", width=150)
    tree_cli.column("dir", width=150)
    tree_cli.pack(fill="x", padx=15)

    # --- FRAME MASCOTAS ---
    frame_masc = tk.LabelFrame(ven_cli, text=" Mascotas asociadas al cliente seleccionado ", font=("Arial", 9, "bold"))
    frame_masc.pack(fill="both", expand=True, padx=15, pady=10)

    tree_masc = ttk.Treeview(frame_masc, columns=("id", "nombre", "especie"), show="headings", height=4)
    tree_masc.heading("id", text="ID Mascota")
    tree_masc.heading("nombre", text="Nombre Mascota")
    tree_masc.heading("especie", text="Especie")
    tree_masc.column("id", width=80)
    tree_masc.column("nombre", width=200)
    tree_masc.column("especie", width=200)
    tree_masc.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    # Contenedor para botones de mascotas
    f_btn_masc = tk.Frame(frame_masc)
    f_btn_masc.pack(side="right", padx=10, pady=10, fill="y")

    btn_add_masc = tk.Button(f_btn_masc, text="+ Agregar Mascota", bg="#8e44ad", fg="white", font=("Arial", 9, "bold"), state="disabled", width=16)
    btn_add_masc.pack(pady=3)

    btn_edit_masc = tk.Button(f_btn_masc, text="✏️ Editar Mascota", bg="#f39c12", fg="white", font=("Arial", 9, "bold"), state="disabled", width=16)
    btn_edit_masc.pack(pady=3)

    btn_del_masc = tk.Button(f_btn_masc, text="🗑️ Eliminar Mascota", bg="#e74c3c", fg="white", font=("Arial", 9, "bold"), state="disabled", width=16)
    btn_del_masc.pack(pady=3)

    # --- EVENTO SELECCIÓN CLIENTE ---
    def al_seleccionar_cliente(event):
        item_sel = tree_cli.selection()
        if item_sel:
            datos_cliente = tree_cli.item(item_sel[0], "values")
            id_cliente = datos_cliente[0]
            nombre_completo = f"{datos_cliente[1]} {datos_cliente[2]}"

            cargar_tabla_mascotas_cliente(tree_masc, id_cliente)

            # Habilitar acciones de cliente
            btn_edit_cli.config(
                state="normal",
                command=lambda: abrir_form_cliente(ven_cli, tree_cli, datos_cliente)
            )
            btn_del_cli.config(
                state="normal",
                command=lambda: eliminar_cliente_action(id_cliente, tree_cli, tree_masc, btn_edit_cli, btn_del_cli, btn_add_masc, btn_edit_masc, btn_del_masc)
            )

            # Habilitar alta de mascotas para este cliente
            btn_add_masc.config(
                state="normal",
                command=lambda: abrir_form_mascota(ven_cli, id_cliente, nombre_completo, tree_masc)
            )

            # Resetear botones de modificación de mascotas
            btn_edit_masc.config(state="disabled")
            btn_del_masc.config(state="disabled")

    # --- EVENTO SELECCIÓN MASCOTA ---
    def al_seleccionar_mascota(event):
        item_sel_m = tree_masc.selection()
        item_sel_c = tree_cli.selection()
        if item_sel_m and item_sel_c:
            datos_mascota = tree_masc.item(item_sel_m[0], "values")
            datos_cliente = tree_cli.item(item_sel_c[0], "values")
            id_cliente = datos_cliente[0]

            btn_edit_masc.config(
                state="normal",
                command=lambda: abrir_form_mascota(ven_cli, id_cliente, f"{datos_cliente[1]} {datos_cliente[2]}", tree_masc, datos_mascota)
            )
            btn_del_masc.config(
                state="normal",
                command=lambda: eliminar_mascota_action(datos_mascota[0], id_cliente, tree_masc)
            )

    tree_cli.bind("<<TreeviewSelect>>", al_seleccionar_cliente)
    tree_masc.bind("<<TreeviewSelect>>", al_seleccionar_mascota)
    cargar_tabla_clientes(tree_cli)


# --- ACCIONES DE ELIMINACIÓN ---
def eliminar_cliente_action(id_cliente, tree_cli, tree_masc, btn_edit_cli, btn_del_cli, btn_add_masc, btn_edit_masc, btn_del_masc):
    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente? Se borrarán sus datos de la base."):
        if cliente_dao.eliminar_cliente(id_cliente):
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            cargar_tabla_clientes(tree_cli)
            # Limpiar tabla mascotas y deshabilitar botones
            for item in tree_masc.get_children():
                tree_masc.delete(item)
            btn_edit_cli.config(state="disabled")
            btn_del_cli.config(state="disabled")
            btn_add_masc.config(state="disabled")
            btn_edit_masc.config(state="disabled")
            btn_del_masc.config(state="disabled")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el cliente.")


def eliminar_mascota_action(id_mascota, id_cliente, tree_masc):
    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta mascota?"):
        if mascota_dao.eliminar_mascota(id_mascota):
            messagebox.showinfo("Éxito", "Mascota eliminada correctamente.")
            cargar_tabla_mascotas_cliente(tree_masc, id_cliente)
        else:
            messagebox.showerror("Error", "No se pudo eliminar la mascota.")


# --- FORMULARIO CLIENTE (CREAR / EDITAR) ---
def abrir_form_cliente(parent, tree_clientes, datos_cliente=None):
    es_edicion = datos_cliente is not None
    v = tk.Toplevel(parent)
    v.title("Editar Cliente" if es_edicion else "Nuevo Cliente")
    v.geometry("350x280")
    v.resizable(False, False)

    tk.Label(v, text="Nombre:").place(x=30, y=30)
    e_nom = tk.Entry(v, width=25); e_nom.place(x=120, y=30)

    tk.Label(v, text="Apellido:").place(x=30, y=70)
    e_ape = tk.Entry(v, width=25); e_ape.place(x=120, y=70)

    tk.Label(v, text="Teléfono:").place(x=30, y=110)
    e_tel = tk.Entry(v, width=25); e_tel.place(x=120, y=110)

    tk.Label(v, text="Email:").place(x=30, y=150)
    e_mail = tk.Entry(v, width=25); e_mail.place(x=120, y=150)

    tk.Label(v, text="Dirección:").place(x=30, y=190)
    e_dir = tk.Entry(v, width=25); e_dir.place(x=120, y=190)

    # Precargar datos si es edición
    if es_edicion:
        e_nom.insert(0, datos_cliente[1])
        e_ape.insert(0, datos_cliente[2])
        e_tel.insert(0, datos_cliente[3])
        e_mail.insert(0, datos_cliente[4])
        e_dir.insert(0, datos_cliente[5])

    def guardar():
        nom, ape, tel, mail, direccion = e_nom.get(), e_ape.get(), e_tel.get(), e_mail.get(), e_dir.get()

        for val, campo in [(nom, "Nombre"), (ape, "Apellido"), (tel, "Teléfono")]:
            ok, msg = validaciones.validar_campo_vacio(val, campo)
            if not ok: messagebox.showwarning("Validación", msg); return

        ok, msg = validaciones.validar_telefono(tel)
        if not ok: messagebox.showwarning("Validación", msg); return

        ok, msg = validaciones.validar_email(mail)
        if not ok: messagebox.showwarning("Validación", msg); return

        if es_edicion:
            id_cliente = datos_cliente[0]
            exito = cliente_dao.actualizar_cliente(id_cliente, nom.strip(), ape.strip(), tel.strip(), mail.strip(), direccion.strip())
            msg_ok = "Cliente actualizado correctamente."
        else:
            exito = cliente_dao.insertar_cliente(nom.strip(), ape.strip(), tel.strip(), mail.strip(), direccion.strip())
            msg_ok = "Cliente registrado correctamente."

        if exito:
            messagebox.showinfo("Éxito", msg_ok)
            v.destroy()
            cargar_tabla_clientes(tree_clientes)
        else:
            messagebox.showerror("Error", "No se pudo guardar la información del cliente.")

    btn = tk.Button(v, text="Actualizar" if es_edicion else "Guardar", bg="#27ae60", fg="white", font=("Arial", 9, "bold"), command=guardar)
    btn.place(x=130, y=230)


# --- FORMULARIO MASCOTA (CREAR / EDITAR) ---
def abrir_form_mascota(parent, id_cliente, nombre_cliente, tree_mascotas, datos_mascota=None):
    es_edicion = datos_mascota is not None
    v = tk.Toplevel(parent)
    v.title(f"Editar Mascota de {nombre_cliente}" if es_edicion else f"Nueva Mascota para {nombre_cliente}")
    v.geometry("350x200")
    v.resizable(False, False)

    especies_db = especie_dao.obtener_especies()
    mapa_especies = {e[1]: e[0] for e in especies_db}

    tk.Label(v, text=f"Dueño: {nombre_cliente}", font=("Arial", 9, "bold")).place(x=30, y=20)

    tk.Label(v, text="Nombre:").place(x=30, y=60)
    e_nom = tk.Entry(v, width=25); e_nom.place(x=120, y=60)

    tk.Label(v, text="Especie:").place(x=30, y=100)
    cb_esp = ttk.Combobox(v, values=list(mapa_especies.keys()), width=22, state="readonly")
    cb_esp.place(x=120, y=100)

    if es_edicion:
        e_nom.insert(0, datos_mascota[1])
        cb_esp.set(datos_mascota[2])

    def guardar():
        nombre = e_nom.get().strip()
        especie_sel = cb_esp.get()

        ok, msg = validaciones.validar_campo_vacio(nombre, "Nombre Mascota")
        if not ok: messagebox.showwarning("Validación", msg); return

        if not especie_sel:
            messagebox.showwarning("Validación", "Debe seleccionar una especie.")
            return

        id_especie = mapa_especies[especie_sel]

        if es_edicion:
            id_mascota = datos_mascota[0]
            exito = mascota_dao.actualizar_mascota(id_mascota, nombre, id_especie)
            msg_ok = "Mascota actualizada correctamente."
        else:
            exito = mascota_dao.insertar_mascota(nombre, id_especie, id_cliente)
            msg_ok = "Mascota agregada correctamente."

        if exito:
            messagebox.showinfo("Éxito", msg_ok)
            v.destroy()
            cargar_tabla_mascotas_cliente(tree_mascotas, id_cliente)
        else:
            messagebox.showerror("Error", "No se pudo procesar la información de la mascota.")

    btn = tk.Button(v, text="Actualizar Mascota" if es_edicion else "Guardar Mascota", bg="#8e44ad", fg="white", font=("Arial", 9, "bold"), command=guardar)
    btn.place(x=110, y=150)