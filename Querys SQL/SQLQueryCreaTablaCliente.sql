-- Creación de la tabla "Cliente"
CREATE TABLE Cliente (
    idCliente int PRIMARY KEY IDENTITY(1,1),
    fechaInscripcion datetime,
	horaInscripcion time(0),
    fechaNacimiento date,
    nombreApellido varchar(255),
	genero varchar(50),
    email varchar(255),
    telefono varchar(20),
    domicilio text,
    dni varchar(20),
	motivoGym VARCHAR(255),
	comoSeEntero VARCHAR(255),
    observaciones text,
	idUsuario varchar(50),
	);