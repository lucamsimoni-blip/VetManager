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
    ven_cli.geometry("800x480")
    ven_cli.resizable(False, False)

    f_top = tk.Frame(ven_cli)
    f_top.pack(fill="x", padx=15, pady=10)

    btn_add_cli = tk.Button(f_top, text="+ Nuevo Cliente", bg="#27ae60", fg="white", font=("Arial", 9, "bold"), command=lambda: abrir_form_cliente(ven_cli, tree_cli))
    btn_add_cli.pack(side="left")

    lbl_info = tk.Label(f_top, text="💡 Seleccioná un cliente para ver o agregar sus mascotas", font=("Arial", 9, "italic"), fg="#7f8c8d")
    lbl_info.pack(side="right")

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

    btn_add_masc = tk.Button(frame_masc, text="+ Agregar Mascota\na este Cliente", bg="#8e44ad", fg="white", state="disabled")
    btn_add_masc.pack(side="right", padx=10, pady=10)

    def al_seleccionar_cliente(event):
        item_sel = tree_cli.selection()
        if item_sel:
            datos_cliente = tree_cli.item(item_sel[0], "values")
            id_cliente = datos_cliente[0]
            cargar_tabla_mascotas_cliente(tree_masc, id_cliente)
            btn_add_masc.config(
                state="normal",
                command=lambda: abrir_form_mascota(ven_cli, id_cliente, f"{datos_cliente[1]} {datos_cliente[2]}", tree_masc)
            )

    tree_cli.bind("<<TreeviewSelect>>", al_seleccionar_cliente)
    cargar_tabla_clientes(tree_cli)

def abrir_form_cliente(parent, tree_clientes):
    v = tk.Toplevel(parent)
    v.title("Nuevo Cliente")
    v.geometry("350x280")

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

    def guardar():
        nom, ape, tel, mail, direccion = e_nom.get(), e_ape.get(), e_tel.get(), e_mail.get(), e_dir.get()

        for val, campo in [(nom, "Nombre"), (ape, "Apellido"), (tel, "Teléfono")]:
            ok, msg = validaciones.validar_campo_vacio(val, campo)
            if not ok: messagebox.showwarning("Validación", msg); return

        ok, msg = validaciones.validar_telefono(tel)
        if not ok: messagebox.showwarning("Validación", msg); return

        ok, msg = validaciones.validar_email(mail)
        if not ok: messagebox.showwarning("Validación", msg); return

        if cliente_dao.insertar_cliente(nom.strip(), ape.strip(), tel.strip(), mail.strip(), direccion.strip()):
            messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
            v.destroy()
            cargar_tabla_clientes(tree_clientes)
        else:
            messagebox.showerror("Error", "No se pudo registrar el cliente.")

    btn = tk.Button(v, text="Guardar", bg="#27ae60", fg="white", command=guardar)
    btn.place(x=130, y=230)

def abrir_form_mascota(parent, id_cliente, nombre_cliente, tree_mascotas):
    v = tk.Toplevel(parent)
    v.title(f"Nueva Mascota para {nombre_cliente}")
    v.geometry("350x200")

    especies_db = especie_dao.obtener_especies()
    mapa_especies = {e[1]: e[0] for e in especies_db}

    tk.Label(v, text=f"Dueño: {nombre_cliente}", font=("Arial", 9, "bold")).place(x=30, y=20)

    tk.Label(v, text="Nombre:").place(x=30, y=60)
    e_nom = tk.Entry(v, width=25); e_nom.place(x=120, y=60)

    tk.Label(v, text="Especie:").place(x=30, y=100)
    cb_esp = ttk.Combobox(v, values=list(mapa_especies.keys()), width=22, state="readonly")
    cb_esp.place(x=120, y=100)

    def guardar():
        nombre = e_nom.get().strip()
        especie_sel = cb_esp.get()

        ok, msg = validaciones.validar_campo_vacio(nombre, "Nombre Mascota")
        if not ok: messagebox.showwarning("Validación", msg); return

        if not especie_sel:
            messagebox.showwarning("Validación", "Debe seleccionar una especie.")
            return

        id_especie = mapa_especies[especie_sel]

        if mascota_dao.insertar_mascota(nombre, id_especie, id_cliente):
            messagebox.showinfo("Éxito", "Mascota agregada correctamente.")
            v.destroy()
            cargar_tabla_mascotas_cliente(tree_mascotas, id_cliente)
        else:
            messagebox.showerror("Error", "No se pudo agregar la mascota.")

    btn = tk.Button(v, text="Guardar Mascota", bg="#8e44ad", fg="white", command=guardar)
    btn.place(x=120, y=150)