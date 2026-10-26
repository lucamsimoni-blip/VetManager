VetManager

Trabajo Integrador ABP — Programación I / Base de Datos, Módulo Programador, Tecnicatura Superior en Desarrollo de Software (ISPC), comisión COM B2.

Integrantes
Luca Simoni — Coordinador / Acceso a datos
Fernando Quarín — Modelo de datos
Gustavo García Quintero — Interfaz
Joaquín Zalazar — Validaciones / Documentación y pruebas

Sistema de escritorio para la gestión de una veterinaria, desarrollado
en Python con Tkinter y MySQL. Permite administrar turnos veterinarios y
gestionar clientes y sus mascotas desde una interfaz gráfica.
Funcionalidades
- Visualizar los turnos registrados en una tabla.
- Agendar nuevos turnos.
- Editar y eliminar turnos.
- Buscar turnos por información relacionada con la mascota, el
  cliente, el veterinario o el estado.
- Registrar, consultar, modificar y eliminar clientes.
- Consultar las mascotas asociadas a un cliente.
- Registrar y administrar mascotas.
- Seleccionar especies, veterinarios, fechas y horarios desde
  formularios.
- Validar algunos datos antes de guardarlos.
- Mantener la información en una base de datos MySQL.
Tecnologías utilizadas
- Python: lógica de la aplicación.
- Tkinter y ttk: interfaz gráfica de escritorio.
- MySQL: almacenamiento de los datos.
- mysql-connector-python: conexión entre Python y MySQL.
- SQL: creación, consulta y modificación de los registros.
- Módulo re: validaciones mediante expresiones regulares.
- Módulo datetime: generación de opciones de fechas y horarios.
Estructura del proyecto
VetManager/
├── main.py
├── schemas.sql
├── db/
│   ├── conexion.py
│   ├── cliente_dao.py
│   ├── especie_dao.py
│   ├── mascota_dao.py
│   └── turno_dao.py
├── views/
│   ├── ventana_clientes.py
│   └── ventana_turnos.py
└── utils/
    └── validaciones.py
La estructura anterior representa los archivos principales del
proyecto que se han utilizado durante su desarrollo. Si el repositorio
contiene otros archivos, pueden agregarse a este árbol.

Requisitos
- Python 3 instalado.
- MySQL Server instalado y en ejecución.
- Una base de datos creada a partir del archivo schemas.sql.
- El paquete mysql-connector-python.
Tkinter suele venir incluido en las instalaciones estándar de Python
para Windows.
Instalación y ejecución
1. Clonar el repositorio
git clone URL_DEL_REPOSITORIO
cd VetManager
Reemplazá URL_DEL_REPOSITORIO por la URL real del repositorio.
2. Crear un entorno virtual (recomendado)
En Windows, desde la carpeta del proyecto:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Si usás el Símbolo del sistema (CMD), la activación es:
.venv\Scripts\activate.bat
3. Instalar la dependencia
python -m pip install mysql-connector-python
4. Crear la base de datos
Ejecutá el contenido de schemas.sql en MySQL Workbench o desde el
cliente de MySQL. El script crea la base vet_manager, las tablas, sus
relaciones y registros de ejemplo.
5. Configurar la conexión
Revisá db/conexion.py. La configuración debe coincidir con tu
instalación de MySQL:
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "TU_USUARIO",
    "password": "TU_CONTRASEÑA",
    "database": "vet_manager"
}
Los valores anteriores son ilustrativos: utilizá tus credenciales
locales. No subas contraseñas reales al repositorio. Para un proyecto
compartido o de producción, conviene leerlas desde variables de entorno
y usar un usuario de MySQL con permisos limitados.
6. Ejecutar la aplicación
Desde la carpeta raíz del proyecto:
python main.py
Organización interna
main.py
Es el punto de entrada de la aplicación. Crea la ventana principal,
muestra el turnero, configura los botones de gestión y conecta las
acciones de la interfaz con las funciones de acceso a datos.
views/
Contiene las ventanas y formularios gráficos: - ventana_turnos.py:
formulario para crear y editar turnos. - ventana_clientes.py: gestión
de clientes y mascotas.
db/
Contiene la conexión con MySQL y las funciones que ejecutan consultas
SQL: - conexion.py: establece la conexión con la base de datos. -
cliente_dao.py: operaciones sobre clientes y consulta de mascotas por
cliente. - especie_dao.py: consulta las especies disponibles. -
mascota_dao.py: operaciones sobre mascotas y consulta de especies. -
turno_dao.py: operaciones sobre turnos, consulta de veterinarios,
reportes y búsquedas.
utils/
- validaciones.py: funciones reutilizables para comprobar campos
  vacíos, formatos básicos de fecha/hora, teléfonos y correos
  electrónicos.
schemas.sql
Define la base de datos, las tablas, las claves primarias, las claves
foráneas, restricciones y datos iniciales.
Modelo de datos
La base de datos incluye cinco tablas principales:
- cliente: datos de contacto del responsable de la mascota.
- especie: catálogo de especies.
- mascota: mascota registrada y referencias a su especie y
  cliente.
- veterinario: datos de los profesionales.
- turno: fecha, hora, motivo, estado y referencias a la mascota
  y al veterinario.
Las claves foráneas relacionan los registros y ayudan a mantener la
integridad de los datos. La tabla turno tiene una restricción única
sobre la combinación de fecha, hora y veterinario, para impedir que un
mismo veterinario tenga dos turnos en el mismo horario.
Flujo general de funcionamiento
1. La persona usuaria interactúa con una ventana de Tkinter.
2. La ventana valida los datos básicos ingresados.
3. La vista llama a una función del módulo DAO correspondiente.
4. El DAO obtiene una conexión mediante db/conexion.py.
5. El DAO ejecuta una consulta SQL y confirma los cambios cuando
   corresponde.
6. La vista informa el resultado y actualiza la tabla si la operación
   tuvo éxito.
Consideraciones
- Las validaciones de fecha y hora que filtran caracteres no
  garantizan por sí solas que la fecha u hora sean válidas.
- Si MySQL rechaza una operación, la interfaz puede mostrar un mensaje
  general de error; para facilitar el diagnóstico, revisá la salida de
  la terminal.
- Antes de presentar o publicar el proyecto, verificá que las
  credenciales no sean reales ni estén expuestas.
- Comprobá que las funciones de la vista y del DAO tengan la misma
  cantidad y orden de parámetros, especialmente en la edición de
  clientes.
- El proyecto utiliza registros de ejemplo para facilitar las pruebas.
  Reemplazalos o quitá el bloque de inserción si necesitás iniciar con
  una base vacía.
Estado del proyecto
Proyecto académico orientado a practicar el desarrollo de una aplicación
de escritorio, el diseño relacional de una base de datos y la
integración entre interfaz gráfica, lógica de aplicación y persistencia
en MySQL.