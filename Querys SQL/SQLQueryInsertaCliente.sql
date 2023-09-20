-- Insertar datos aleatorios para 10 clientes
INSERT INTO Cliente (fechaInscripcion, fechaNacimiento, nombreApellido, genero, email, telefono, domicilio, dni, requiereInstructor, pesoInicial, objetivo, observaciones, idUsuario, horaRegistro)
VALUES
  ('2023-09-12', '1990-05-15', 'Juan Perez', 'Hombre', 'juanperez@example.com', '123456789', 'Calle 123, Salta, Argentina', '12345678', 1, 75, 'Bajar de Peso', 'Sin observaciones', 1, '2023-09-12 19:14:29.270'),
  ('2023-09-13', '1985-02-20', 'Maria Rodriguez', 'Mujer', 'mariarodriguez@example.com', '987654321', 'Avenida 456, Salta, Argentina', '23456789', 0, 65, 'Mantener', 'Observación 1', 2, '2023-09-13 10:30:45.150'),
  ('2023-09-14', '1995-09-01', 'Carlos Sanchez', 'Hombre', 'carlossanchez@example.com', '555555555', 'Plaza 789, Salta, Argentina', '34567890', 1, 85, 'Subir de Peso', 'Observación 2', 3, '2023-09-14 15:20:10.430'),
  ('2023-09-15', '1980-11-10', 'Luisa Gomez', 'Mujer', 'luisagomez@example.com', '111111111', 'Callejon 101, Salta, Argentina', '45678901', 0, 55, 'Bajar de Peso', 'Observación 3', 4, '2023-09-15 08:45:56.590'),
  ('2023-09-16', '1998-07-05', 'Ana Martinez', 'Mujer', 'anamartinez@example.com', '222222222', 'Paseo 555, Salta, Argentina', '56789012', 1, 70, 'Mantener', 'Observación 4', 5, '2023-09-16 14:10:30.780'),
  ('2023-09-17', '1978-03-25', 'Pedro Lopez', 'Hombre', 'pedrolopez@example.com', '999999999', 'Camino 222, Salta, Argentina', '67890123', 0, 95, 'Subir de Peso', 'Observación 5', 1, '2023-09-17 12:05:20.670'),
  ('2023-09-18', '1992-12-15', 'Laura Fernandez', 'Mujer', 'laurafernandez@example.com', '777777777', 'Avenida 333, Salta, Argentina', '78901234', 1, 60, 'Bajar de Peso', 'Observación 6', 2, '2023-09-18 17:55:40.920'),
  ('2023-09-19', '1987-08-30', 'Jorge Ramirez', 'Hombre', 'jorgeramirez@example.com', '888888888', 'Calle 444, Salta, Argentina', '89012345', 0, 80, 'Mantener', 'Observación 7', 3, '2023-09-19 09:40:15.360'),
  ('2023-09-20', '2000-01-12', 'Silvia Torres', 'Mujer', 'silviatorres@example.com', '333333333', 'Plaza 111, Salta, Argentina', '90123456', 1, 50, 'Bajar de Peso', 'Observación 8', 4, '2023-09-20 13:25:05.540'),
  ('2023-09-21', '1993-06-18', 'Daniel Gonzalez', 'Hombre', 'danielgonzalez@example.com', '666666666', 'Callejon 999, Salta, Argentina', '01234567', 0, 70, 'Mantener', 'Observación 9', 5, '2023-09-21 11:15:30.220');
