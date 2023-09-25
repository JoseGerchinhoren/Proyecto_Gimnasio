-- Insertar datos aleatorios de pagos para clientes
DECLARE @StartDate DATE = '2023-05-01'
DECLARE @EndDate DATE = GETDATE()
DECLARE @CurrentDate DATE = @StartDate

-- Variables para idCliente desde 1056 hasta 1585
DECLARE @MinIdCliente INT = 1056
DECLARE @MaxIdCliente INT = 1585

WHILE @CurrentDate <= @EndDate
BEGIN
  -- Verificar si el día de la semana es de lunes a viernes (1 a 5)
  IF DATEPART(WEEKDAY, @CurrentDate) BETWEEN 2 AND 6
  BEGIN
    -- Generar datos de pago para cada idCliente
    DECLARE @idCliente INT = @MinIdCliente

    WHILE @idCliente <= @MaxIdCliente
    BEGIN
      INSERT INTO Pago (idCliente, idUsuario, fechaPago, horarioPago, montoPago, metodoPago, detallePago)
      VALUES
        (
          @idCliente,
          CAST((RAND() * 5) + 1 AS INT), -- Generar idUsuario aleatorio entre 1 y 5
          @CurrentDate,
          CONVERT(TIME, SYSDATETIME()),
          7000,
          CASE
            WHEN RAND() <= 0.2 THEN 'Efectivo'
            WHEN RAND() <= 0.4 THEN 'Transferencia'
            WHEN RAND() <= 0.6 THEN 'Tarjeta de Crédito'
            WHEN RAND() <= 0.8 THEN 'Tarjeta de Débito'
            ELSE 'Otro'
          END, -- Seleccionar método de pago aleatorio
          'Cuota mensual'
        )
      SET @idCliente = @idCliente + 1
    END
  END
  SET @CurrentDate = DATEADD(DAY, 1, @CurrentDate)
END