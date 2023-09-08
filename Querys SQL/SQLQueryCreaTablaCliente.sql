-- Creación de la tabla "cliente"
CREATE TABLE Cliente (
    idCliente int PRIMARY KEY IDENTITY(1,1),
    fecha_inscripcion date,
    fecha_nacimiento date,
    nombre_apellido varchar(255),
    email varchar(255),
    telefono varchar(20),
    domicilio text,
    dni varchar(20),
    requiere_instructor tinyint,
    peso_inicial int,
    objetivo varchar(50),
    observaciones text
);