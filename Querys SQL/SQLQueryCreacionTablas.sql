-- Creación de la tabla "cliente"
CREATE TABLE cliente (
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

-- Creación de la tabla "pago"
CREATE TABLE pago (
    id int PRIMARY KEY IDENTITY(1,1),
    fechaPago date,
    idCliente int,
    nombreApellidoCliente varchar(255),
    montoPago decimal(10,2),
    metodoPago varchar(50),
    detallePago varchar(255)
);
