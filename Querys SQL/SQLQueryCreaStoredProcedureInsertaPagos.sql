CREATE PROCEDURE [dbo].[InsertarPago]
    @fechaPago DATE,
    @idCliente INT,
    @montoPago INT,
    @metodoPago VARCHAR(50),
    @detallePago VARCHAR(255),
    @idUsuario INT
AS
BEGIN
    DECLARE @horario_pago datetime;
    SET @horario_pago = GETDATE(); -- Obtiene la hora actual

    INSERT INTO Pago (fechaPago, horarioPago, idCliente, montoPago, metodoPago, detallePago, idUsuario)
    VALUES (@fechaPago, @horario_pago, @idCliente, @montoPago, @metodoPago, @detallePago, @idUsuario);
END;
