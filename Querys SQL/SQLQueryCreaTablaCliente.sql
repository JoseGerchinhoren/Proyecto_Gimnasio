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
	motivoGym VARCHAR(255),
	comoSeEntero VARCHAR(255),
    observaciones text,
	idUsuario varchar(50),
	);