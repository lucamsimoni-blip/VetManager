CREATE DATABASE IF NOT EXISTS vet_manager;
USE vet_manager;

CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    direccion VARCHAR(150)
);

-- Nueva tabla creada por pedido de la profe
CREATE TABLE especie (
    id_especie INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE mascota (
    id_mascota INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_especie INT NOT NULL,
    id_cliente INT NOT NULL,
    CONSTRAINT fk_mascota_especie FOREIGN KEY (id_especie) 
        REFERENCES especie(id_especie) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_mascota_cliente FOREIGN KEY (id_cliente) 
        REFERENCES cliente(id_cliente) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE veterinario (
    id_veterinario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    especialidad VARCHAR(50)
);

CREATE TABLE turno (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo VARCHAR(200) NOT NULL,
    estado VARCHAR(20) NOT NULL,
    id_veterinario INT NOT NULL,
    id_mascota INT NOT NULL,
    CONSTRAINT fk_turno_veterinario FOREIGN KEY (id_veterinario) 
        REFERENCES veterinario(id_veterinario) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_turno_mascota FOREIGN KEY (id_mascota) 
        REFERENCES mascota(id_mascota) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Datos iniciales recomendados para poblar el ComboBox de especies en Tkinter
INSERT INTO especie (nombre) VALUES 
('Perro'), 
('Gato'), 
('Ave'), 
('Reptil'), 
('Roedor');