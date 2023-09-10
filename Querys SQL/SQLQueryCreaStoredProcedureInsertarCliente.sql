-- Creación del procedimiento almacenado para insertar clientes
CREATE PROCEDURE InsertarCliente (
    @fecha_inscripcion date,
    @fecha_nacimiento date,
    @nombre_apellido varchar(255),
    @email varchar(255),
    @telefono varchar(20),
    @domicilio text,
    @dni varchar(20),
    @requiere_instructor tinyint,
    @peso_inicial int,
    @objetivo varchar(50),
    @observaciones text,
    @id_usuario int
)
AS
BEGIN
    DECLARE @hora_registro datetime;
    SET @hora_registro = GETDATE(); -- Obtiene la hora actual

    INSERT INTO Cliente (
        fechaInscripcion,
        fechaNacimiento,
        nombreApellido,
        email,
        telefono,
        domicilio,
        dni,
        requiereInstructor,
        pesoInicial,
        objetivo,
        observaciones,
        idUsuario,
        horaRegistro
    )
    VALUES (
        @fecha_inscripcion,
        @fecha_nacimiento,
        @nombre_apellido,
        @email,
        @telefono,
        @domicilio,
        @dni,
        @requiere_instructor,
        @peso_inicial,
        @objetivo,
        @observaciones,
        @id_usuario,
        @hora_registro
    );
END;