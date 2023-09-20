-- Creación de la tabla "cliente"
CREATE TABLE Cliente (
    idCliente int PRIMARY KEY IDENTITY(1,1),
    fechaInscripcion datetime,
    fechaNacimiento date,
    nombreApellido varchar(255),
    email varchar(255),
    telefono varchar(20),
    domicilio text,
    dni varchar(20),
    requiereInstructor tinyint,
    pesoInicial int,
    objetivo varchar(50),
    observaciones text,
	idUsuario varchar(50),
	);