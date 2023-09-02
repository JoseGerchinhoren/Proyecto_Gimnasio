-- Crear tabla para registrar modificaciones en clientes
CREATE TABLE ModificacionesClientes (
    idModificacion INT PRIMARY KEY IDENTITY(1,1),
    idCliente INT,
    fechaModificacion DATETIME DEFAULT GETDATE(),
    usuarioModificacion VARCHAR(255),
    CONSTRAINT FK_Cliente_ModificacionesClientes FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente)
);

-- Crear tabla para registrar modificaciones en pagos
CREATE TABLE ModificacionesPagos (
    idModificacion INT PRIMARY KEY IDENTITY(1,1),
    idPago INT,
    fechaModificacion DATETIME DEFAULT GETDATE(),
    usuarioModificacion VARCHAR(255),
    CONSTRAINT FK_Pago_ModificacionesPagos FOREIGN KEY (idPago) REFERENCES Pago(idPago)
);
