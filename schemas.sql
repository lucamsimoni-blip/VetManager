CREATE DATABASE IF NOT EXISTS vet_manager;
USE vet_manager;

-- 1. TABLA CLIENTE 
CREATE TABLE cliente (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    direccion VARCHAR(150)
);

INSERT INTO cliente (nombre, apellido, telefono, email, direccion) VALUES 
('Juan', 'Pérez', '3547123456', 'juan.perez@email.com', 'San Martín 123'),
('María', 'Gómez', '3547987654', 'maria.gomez@email.com', 'Belgrano 456'),
('Carlos', 'López', '3547112233', 'carlos.lopez@email.com', 'Sarmiento 789'),
('Ana', 'Martínez', '3547445566', 'ana.martinez@email.com', 'Mitre 321'),
('Luis', 'Rodríguez', '3547778899', 'luis.rodriguez@email.com', 'Rivadavia 654'),
('Laura', 'Fernández', '3547334455', 'laura.fernandez@email.com', 'Alvear 987'),
('Pedro', 'González', '3547665544', 'pedro.gonzalez@email.com', 'San Lorenzo 111'),
('Sofía', 'Díaz', '3547223344', 'sofia.diaz@email.com', 'Colon 222'),
('Jorge', 'Álvarez', '3547990011', 'jorge.alvarez@email.com', 'Urquiza 333'),
('Lucía', 'Romero', '3547556677', 'lucia.romero@email.com', 'Pringles 444');


-- 2. TABLA ESPECIE 
CREATE TABLE especie (
    id_especie INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO especie (nombre) VALUES 
('Perro'), 
('Gato'), 
('Ave'), 
('Reptil'), 
('Roedor');


-- 3. TABLA MASCOTA 
CREATE TABLE mascota (
    id_mascota INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    id_especie INT NOT NULL,
    id_cliente INT NOT NULL,
    CONSTRAINT fk_mascota_especie FOREIGN KEY (id_especie) 
        REFERENCES especie(id_especie) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_mascota_cliente FOREIGN KEY (id_cliente) 
        REFERENCES cliente(id_cliente) ON DELETE RESTRICT ON UPDATE CASCADE
);

INSERT INTO mascota (nombre, id_especie, id_cliente) VALUES 
('Firulais', 1, 1),
('Michi', 2, 2),
('Paco', 3, 3),
('Roco', 1, 4),
('Luna', 2, 5),
('Bolt', 1, 6),
('Nina', 2, 7),
('Pepe', 3, 8),
('Coco', 5, 9),
('Simba', 2, 10);


-- 4. TABLA VETERINARIO 
CREATE TABLE veterinario (
    id_veterinario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    especialidad VARCHAR(50)
);

INSERT INTO veterinario (nombre, apellido, especialidad) VALUES 
('Roberto', 'Sánchez', 'Cirugía General'),
('Elena', 'Blanco', 'Medicina Felina'),
('Martín', 'Acosta', 'Traumatología'),
('Carla', 'Benítez', 'Dermatología'),
('Esteban', 'Paz', 'Cardiología'),
('Valeria', 'Ríos', 'Oftalmología'),
('Diego', 'Navarro', 'Oncología'),
('Florencia', 'Molina', 'Animales Exóticos'),
('Gabriel', 'Ortiz', 'Odontología'),
('Mariana', 'Iglesias', 'Medicina General');


-- 5. TABLA TURNO  
CREATE TABLE turno (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo VARCHAR(200) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'Pendiente' CHECK (estado IN ('Pendiente', 'Atendido', 'Cancelado')),
    id_veterinario INT NOT NULL,
    id_mascota INT NOT NULL,
    -- Evita que el mismo veterinario tenga un turno a la misma fecha y hora exacta
    CONSTRAINT uk_turno_vet_horario UNIQUE (fecha, hora, id_veterinario),
    CONSTRAINT fk_turno_veterinario FOREIGN KEY (id_veterinario) 
        REFERENCES veterinario(id_veterinario) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_turno_mascota FOREIGN KEY (id_mascota) 
        REFERENCES mascota(id_mascota) ON DELETE RESTRICT ON UPDATE CASCADE
);

INSERT INTO turno (fecha, hora, motivo, estado, id_veterinario, id_mascota) VALUES 
('2026-11-01', '09:00:00', 'Control anual y vacunas', 'Pendiente', 1, 1),
('2026-11-01', '10:00:00', 'Dolor estomacal', 'Pendiente', 2, 2),
('2026-11-01', '11:00:00', 'Revisión de ala lastimada', 'Atendido', 8, 3),
('2026-11-02', '09:30:00', 'Chequeo post-operatorio', 'Pendiente', 3, 4),
('2026-11-02', '10:30:00', 'Problemas en la piel', 'Cancelado', 4, 5),
('2026-11-03', '15:00:00', 'Control cardíaco', 'Pendiente', 5, 6),
('2026-11-03', '16:00:00', 'Infección en el ojo', 'Pendiente', 6, 7),
('2026-11-04', '09:00:00', 'Consulta general', 'Pendiente', 10, 8),
('2026-11-04', '10:15:00', 'Control de peso y dieta', 'Pendiente', 10, 9),
('2026-11-05', '11:30:00', 'Vacunación antirrábica', 'Pendiente', 2, 10);

