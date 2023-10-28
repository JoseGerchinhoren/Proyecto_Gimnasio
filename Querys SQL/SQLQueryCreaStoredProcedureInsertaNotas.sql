CREATE PROCEDURE GuardarNota
    @idUsuario INT,
    @fecha DATE,
    @nota TEXT
AS
BEGIN
    INSERT INTO Notas (idUsuario, fecha, nota)
    VALUES (@idUsuario, @fecha, @nota);
END;
