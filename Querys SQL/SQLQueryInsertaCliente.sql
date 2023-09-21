-- Insertar datos aleatorios para 20 clientes
INSERT INTO Cliente (fechaInscripcion, horaInscripcion, fechaNacimiento, nombreApellido, genero, email, telefono, domicilio, dni, requiereInstructor, pesoInicial, objetivo, observaciones, idUsuario)
VALUES
  ('2023-09-12', '19:14:29', '1990-05-15', 'Juan Perez', 'Hombre', 'juanperez@example.com', '123456789', 'Calle 123, Salta, Argentina', '12345678', 1, 75, 'Bajar de Peso', 'Sin observaciones', 1),
  ('2023-09-13', '10:30:45', '1985-02-20', 'Maria Rodriguez', 'Mujer', 'mariarodriguez@example.com', '987654321', 'Avenida 456, Salta, Argentina', '23456789', 0, 65, 'Mantener', 'Observación 1', 2),
  ('2023-09-14', '15:20:10', '1995-09-01', 'Carlos Sanchez', 'Hombre', 'carlossanchez@example.com', '555555555', 'Plaza 789, Salta, Argentina', '34567890', 1, 85, 'Subir de Peso', 'Observación 2', 3),
  ('2023-09-15', '08:45:56', '1980-11-10', 'Luisa Gomez', 'Mujer', 'luisagomez@example.com', '111111111', 'Callejon 101, Salta, Argentina', '45678901', 0, 55, 'Bajar de Peso', 'Observación 3', 4),
  ('2023-09-16', '14:10:30', '1998-07-05', 'Ana Martinez', 'Mujer', 'anamartinez@example.com', '222222222', 'Paseo 555, Salta, Argentina', '56789012', 1, 70, 'Mantener', 'Observación 4', 5),
  ('2023-09-17', '12:05:20', '1978-03-25', 'Pedro Lopez', 'Hombre', 'pedrolopez@example.com', '999999999', 'Camino 222, Salta, Argentina', '67890123', 0, 95, 'Subir de Peso', 'Observación 5', 1),
  ('2023-09-18', '17:55:40', '1992-12-15', 'Laura Fernandez', 'Mujer', 'laurafernandez@example.com', '777777777', 'Avenida 333, Salta, Argentina', '78901234', 1, 60, 'Bajar de Peso', 'Observación 6', 2),
  ('2023-09-19', '09:40:15', '1987-08-30', 'Jorge Ramirez', 'Hombre', 'jorgeramirez@example.com', '888888888', 'Calle 444, Salta, Argentina', '89012345', 0, 80, 'Mantener', 'Observación 7', 3),
  ('2023-09-20', '13:25:05', '2000-01-12', 'Silvia Torres', 'Mujer', 'silviatorres@example.com', '333333333', 'Plaza 111, Salta, Argentina', '90123456', 1, 50, 'Bajar de Peso', 'Observación 8', 4),
  ('2023-09-21', '11:15:30', '1993-06-18', 'Daniel Gonzalez', 'Hombre', 'danielgonzalez@example.com', '666666666', 'Callejon 999, Salta, Argentina', '01234567', 0, 70, 'Mantener', 'Observación 9', 5),
  ('2023-09-22', '09:30:15', '1994-04-08', 'Marcelo Rodriguez', 'Hombre', 'marcelorodriguez@example.com', '555555555', 'Avenida 777, Salta, Argentina', '12345678', 0, 70, 'Subir de Peso', 'Observación 10', 1),
  ('2023-09-23', '14:45:20', '1988-12-28', 'Carmen Lopez', 'Mujer', 'carmenlopez@example.com', '999999999', 'Calle 555, Salta, Argentina', '23456789', 1, 60, 'Bajar de Peso', 'Observación 11', 2),
  ('2023-09-24', '11:10:35', '1996-09-15', 'Gabriel Fernandez', 'Hombre', 'gabrielfernandez@example.com', '777777777', 'Callejon 888, Salta, Argentina', '34567890', 0, 80, 'Mantener', 'Observación 12', 3),
  ('2023-09-25', '16:20:55', '1982-03-05', 'Elena Martinez', 'Mujer', 'elenamartinez@example.com', '888888888', 'Plaza 111, Salta, Argentina', '45678901', 1, 55, 'Bajar de Peso', 'Observación 13', 4),
  ('2023-09-26', '08:05:40', '1997-07-20', 'Rodrigo Gonzalez', 'Hombre', 'rodrigogonzalez@example.com', '333333333', 'Avenida 222, Salta, Argentina', '56789012', 0, 90, 'Subir de Peso', 'Observación 14', 5),
  ('2023-09-27', '12:55:10', '1975-11-30', 'Marta Silva', 'Mujer', 'martasilva@example.com', '666666666', 'Camino 333, Salta, Argentina', '67890123', 1, 65, 'Bajar de Peso', 'Observación 15', 1),
  ('2023-09-28', '14:30:25', '1991-08-12', 'Pablo Ramirez', 'Hombre', 'pabloramirez@example.com', '222222222', 'Paseo 444, Salta, Argentina', '78901234', 0, 75, 'Mantener', 'Observación 16', 2),
  ('2023-09-29', '10:15:55', '1986-02-25', 'Lorena Torres', 'Mujer', 'lorenatorres@example.com', '111111111', 'Calle 666, Salta, Argentina', '89012345', 1, 70, 'Bajar de Peso', 'Observación 17', 3),
  ('2023-09-30', '13:40:30', '1999-05-18', 'Carlos Gomez', 'Hombre', 'carlosgomez@example.com', '123123123', 'Avenida 999, Salta, Argentina', '90123456', 0, 85, 'Mantener', 'Observación 18', 4),
  ('2023-10-01', '16:00:45', '1989-10-02', 'Susana Rodriguez', 'Mujer', 'susanarodriguez@example.com', '987987987', 'Plaza 777, Salta, Argentina', '01234567', 1, 75, 'Bajar de Peso', 'Observación 19', 5);