-- Creación de la tabla "pago"
CREATE TABLE Pago (
    id int PRIMARY KEY IDENTITY(1,1),
    fechaPago date,
    idCliente int,
    nombreApellidoCliente varchar(255),
    montoPago decimal(10,2),
    metodoPago varchar(50),
    detallePago varchar(255)
);
