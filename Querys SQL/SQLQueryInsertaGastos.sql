-- Generar 100 registros de gastos aleatorios en el rango de fechas
DECLARE @counter INT = 1
DECLARE @categorias NVARCHAR(MAX) = 'Mantenimiento,Suministros,Alquiler,Insumos,Pago Empleados,Otro'
DECLARE @metodosPago NVARCHAR(MAX) = 'Efectivo,Transferencia,Tarjeta,Otro'
DECLARE @motivos NVARCHAR(MAX) = 'Limpieza,Pintura,Cemento,Otro'
DECLARE @lugares NVARCHAR(MAX) = 'Pintureria,Tienda de Suministros,Empresa de Alquiler,Tienda de Insumos,Oficina Central,Otro'

WHILE @counter <= 100
BEGIN
    INSERT INTO Gasto (fecha, motivo, lugar, monto, metodoPago, categoria, observacion)
    VALUES (
        DATEADD(day, -RAND() * 154, '2023-10-01'), -- Fecha aleatoria entre mayo y octubre de 2023
        (SELECT TOP 1 value FROM STRING_SPLIT(@motivos, ',') ORDER BY NEWID()), -- Motivo aleatorio
        CASE
            WHEN (SELECT TOP 1 value FROM STRING_SPLIT(@motivos, ',') ORDER BY NEWID()) = 'Pintura' THEN 'Pintureria'
            WHEN (SELECT TOP 1 value FROM STRING_SPLIT(@motivos, ',') ORDER BY NEWID()) = 'Suministros' THEN 'Tienda de Suministros'
            WHEN (SELECT TOP 1 value FROM STRING_SPLIT(@motivos, ',') ORDER BY NEWID()) = 'Alquiler' THEN 'Empresa de Alquiler'
            WHEN (SELECT TOP 1 value FROM STRING_SPLIT(@motivos, ',') ORDER BY NEWID()) = 'Insumos' THEN 'Tienda de Insumos'
            ELSE (SELECT TOP 1 value FROM STRING_SPLIT(@lugares, ',') ORDER BY NEWID())
        END, -- Lugar aleatorio dependiendo del motivo
        100 + CAST(RAND() * 9900 AS INT), -- Monto aleatorio entre 100 y 10,000
        (SELECT TOP 1 value FROM STRING_SPLIT(@metodosPago, ',') ORDER BY NEWID()), -- Método de pago aleatorio
        (SELECT TOP 1 value FROM STRING_SPLIT(@categorias, ',') ORDER BY NEWID()), -- Categoría aleatoria
        'Observación' + CAST(@counter AS NVARCHAR(10)) -- Observación única para cada registro
    )

    SET @counter = @counter + 1
END
