CREATE TABLE PagosEliminados (
    idPagoEliminado INT IDENTITY(1,1) PRIMARY KEY,
	fechaEliminacion DATETIME NOT NULL,
    idPago INT NOT NULL,
    idCliente INT NOT NULL,
    idUsuario INT NOT NULL,
    fechaPago DATETIME NOT NULL,
    horarioPago TIME NOT NULL,
    montoPago DECIMAL(10, 2) NOT NULL,
    metodoPago NVARCHAR(255) NOT NULL,
    detallePago NVARCHAR(MAX) NOT NULL
);
