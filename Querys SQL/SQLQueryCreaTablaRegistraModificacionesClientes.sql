-- Crear tabla para registrar modificaciones en clientes
CREATE TABLE ModificacionesClientes (
    idModificacionCliente INT PRIMARY KEY IDENTITY(1,1),
    idCliente INT,
    fechaModificacion DATETIME DEFAULT GETDATE(),
    idUsuario INT,
	campoModificado varchar(50),
	valorAnterior VARCHAR(500)
);