-- MIGRACIÓN: evitar turnos simultáneos para veterinarios y mascotas.
-- Ejecutar UNA SOLA VEZ sobre una base vet_manager ya existente.
-- Antes de ejecutar, comprobar que no haya duplicados activos:
--
-- SELECT fecha, hora, id_veterinario, COUNT(*) AS cantidad
-- FROM turno
-- WHERE estado <> 'Cancelado'
-- GROUP BY fecha, hora, id_veterinario
-- HAVING COUNT(*) > 1;
--
-- SELECT fecha, hora, id_mascota, COUNT(*) AS cantidad
-- FROM turno
-- WHERE estado <> 'Cancelado'
-- GROUP BY fecha, hora, id_mascota
-- HAVING COUNT(*) > 1;
--
-- Si alguna consulta devuelve filas, resolver esos duplicados antes
-- de continuar. La migración reemplaza el índice anterior y agrega
-- restricciones que ignoran los turnos cancelados.

USE vet_manager;

ALTER TABLE turno
    DROP INDEX uk_turno_vet_horario,
    ADD COLUMN id_veterinario_activo INT
        GENERATED ALWAYS AS (
            CASE WHEN estado <> 'Cancelado' THEN id_veterinario ELSE NULL END
        ) STORED,
    ADD COLUMN id_mascota_activa INT
        GENERATED ALWAYS AS (
            CASE WHEN estado <> 'Cancelado' THEN id_mascota ELSE NULL END
        ) STORED,
    ADD CONSTRAINT uk_turno_vet_horario_activo
        UNIQUE (fecha, hora, id_veterinario_activo),
    ADD CONSTRAINT uk_turno_mascota_horario_activo
        UNIQUE (fecha, hora, id_mascota_activa);
