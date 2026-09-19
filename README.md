VetManager

Aplicación de escritorio para la gestión de turnos de una veterinaria de barrio: registro de clientes, mascotas, veterinarios y turnos, pensada para reemplazar los cuadernos y planillas sueltas que suelen usarse en este tipo de negocios.

Trabajo Integrador ABP — Programación I / Base de Datos, Módulo Programador, Tecnicatura Superior en Desarrollo de Software (ISPC), comisión COM B2.

Integrantes
Luca Simoni — Coordinador / Acceso a datos
Fernando Quarín — Modelo de datos
Gustavo Shadow — Interfaz
Joaquín Zalazar — Validaciones / Documentación y pruebas


Tecnologías utilizadas
Lenguaje: Python 3.10+
Interfaz gráfica: Tkinter + ttk (biblioteca estándar)
Base de datos: MySQL
Conector: mysql-connector-python
Control de versiones: Git / GitHub


Estructura del proyecto
vetmanager/
├── conexion.py       # Conexión a la base de datos MySQL
├── acceso_datos.py   # Sentencias SQL (SELECT, INSERT, UPDATE, DELETE)
├── interfaz.py        # Interfaz gráfica Tkinter/ttk y punto de entrada
├── schema.sql          # Esquema completo (DDL) y datos de prueba
└── README.md



Funcionalidades principales

El modelo de datos completo contempla 4 entidades: Cliente, Mascota, Turno y Veterinario. Las funcionalidades planificadas son:

Gestión de Clientes (alta, listado, modificación, baja)
Gestión de Mascotas (alta, listado, modificación, baja) — en desarrollo
Gestión de Turnos (alta, listado, modificación, baja, asignación a veterinario)
Listado combinado Mascota-Cliente mediante JOIN
Búsqueda/filtro de mascotas por nombre
Estado actual del desarrollo

Se está implementando la primera funcionalidad completa, Gestión de Mascotas, siguiendo la recomendación del equipo docente de terminar un módulo entero antes de avanzar con el resto:

 Esquema de base de datos (schema.sql) con las 4 entidades y datos de prueba para Cliente y Mascota
 Conexión a MySQL (conexion.py)
 Acceso a datos de Mascota: alta, listado con JOIN a Cliente, filtro por nombre, modificación y baja (acceso_datos.py)
 Interfaz gráfica de Mascotas: listado (Treeview), filtro, formulario de alta/edición con combo de cliente, confirmación de baja (interfaz.py)
 Gestión de Clientes (próxima iteración)
 Gestión de Turnos y asignación a Veterinario (próxima iteración)
 Roles de acceso e integridad avanzada en el SGBD
Cómo ejecutar (una vez configurada la base de datos)
Crear la base de datos y las tablas ejecutando schema.sql en MySQL.
Completar el usuario y la contraseña de conexión en conexion.py.
Instalar la dependencia: pip install mysql-connector-python
Ejecutar: python interfaz.py