-- Insertar datos aleatorios para 20 clientes con fechas de inscripción desde 2023-05-01 hasta la fecha de hoy (lunes a viernes)
DECLARE @StartDate DATE = '2023-05-01'
DECLARE @EndDate DATE = GETDATE()
DECLARE @CurrentDate DATE = @StartDate

WHILE @CurrentDate <= @EndDate
BEGIN
  -- Verificar si el día de la semana es de lunes a viernes (1 a 5)
  IF DATEPART(WEEKDAY, @CurrentDate) BETWEEN 2 AND 6
  BEGIN
    INSERT INTO Cliente (fechaInscripcion, horaInscripcion, fechaNacimiento, nombreApellido, genero, email, telefono, domicilio, dni, requiereInstructor, pesoInicial, objetivo, observaciones, idUsuario)
    VALUES
      (@CurrentDate, CONVERT(TIME, SYSDATETIME()), '1990-05-15', 'Juan Perez', 'Hombre', 'juanperez@example.com', '123456789', 'Calle 123, Salta, Argentina', '12345678', 1, 75, 'Bajar de Peso', 'Sin observaciones', 1),
      (@CurrentDate, CONVERT(TIME, SYSDATETIME()), '1985-02-20', 'Maria Rodriguez', 'Mujer', 'mariarodriguez@example.com', '987654321', 'Avenida 456, Salta, Argentina', '23456789', 0, 65, 'Mantener', 'Observación 1', 2),
      (@CurrentDate, CONVERT(TIME, SYSDATETIME()), '1995-09-01', 'Carlos Sanchez', 'Hombre', 'carlossanchez@example.com', '555555555', 'Plaza 789, Salta, Argentina', '34567890', 1, 85, 'Subir de Peso', 'Observación 2', 3),
      (@CurrentDate, CONVERT(TIME, SYSDATETIME()), '1980-11-10', 'Luisa Gomez', 'Mujer', 'luisagomez@example.com', '111111111', 'Callejon 101, Salta, Argentina', '45678901', 0, 55, 'Bajar de Peso', 'Observación 3', 4),
      (@CurrentDate, CONVERT(TIME, SYSDATETIME()), '1998-07-05', 'Ana Martinez', 'Mujer', 'anamartinez@example.com', '222222222', 'Paseo 555, Salta, Argentina', '56789012', 1, 70, 'Mantener', 'Observación 4', 5)
    -- Agrega más registros aquí si es necesario
  END
  SET @CurrentDate = DATEADD(DAY, 1, @CurrentDate)
END