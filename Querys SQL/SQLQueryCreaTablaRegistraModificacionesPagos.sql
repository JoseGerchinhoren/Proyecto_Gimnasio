-- Crear tabla para registrar modificaciones en pagos
CREATE TABLE ModificacionesPagos (
    idModificacionPago INT PRIMARY KEY IDENTITY(1,1),
    idPago INT,
    fechaModificacion DATETIME DEFAULT GETDATE(),
    idUsuario INT,
	campoModificado varchar(50),
	valorAnterior VARCHAR(500)
);
