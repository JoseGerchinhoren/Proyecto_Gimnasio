-- Creación de la tabla "pago"
CREATE TABLE Pago (
    idPago int PRIMARY KEY IDENTITY(1,1),
    idCliente int,
	idUsuario int,
	fechaPago date,
	horarioPago time(0),
    montoPago decimal(10,2),
    metodoPago varchar(50),
    detallePago varchar(255)
);
