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

CREATE TABLE mascota (
    id_mascota INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    especie VARCHAR(30) NOT NULL,
    id_cliente INT NOT NULL,
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