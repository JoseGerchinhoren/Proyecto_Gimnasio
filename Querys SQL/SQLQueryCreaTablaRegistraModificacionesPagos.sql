-- Crear tabla para registrar modificaciones en pagos
CREATE TABLE ModificacionesPagos (
    idModificacionPago INT PRIMARY KEY IDENTITY(1,1),
    idPago INT,
    fechaModificacion DATETIME DEFAULT GETDATE(),
    usuarioModificacion VARCHAR(255),
    CONSTRAINT FK_Pago_ModificacionesPagos FOREIGN KEY (idPago) REFERENCES Pago(idPago),
	valorAnterior VARCHAR(500)
);
