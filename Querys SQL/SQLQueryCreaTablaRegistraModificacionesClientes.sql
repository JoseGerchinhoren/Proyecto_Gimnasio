-- Crear tabla para registrar modificaciones en clientes
CREATE TABLE ModificacionesClientes (
    idModificacionCliente INT PRIMARY KEY IDENTITY(1,1),
    idCliente INT,
    fechaModificacion DATETIME DEFAULT GETDATE(),
    usuarioModificacion VARCHAR(255),
    CONSTRAINT FK_Cliente_ModificacionesClientes FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente),
	valorAnterior VARCHAR(500)
);