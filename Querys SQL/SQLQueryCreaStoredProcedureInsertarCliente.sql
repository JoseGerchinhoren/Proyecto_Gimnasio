CREATE PROCEDURE [dbo].[InsertarCliente] (
    @fecha_inscripcion datetime,
    @fecha_nacimiento date,
    @nombre_apellido varchar(255),
    @genero varchar(50),
    @email varchar(255),
    @telefono varchar(20),
    @domicilio text,
    @dni varchar(20),
    @motivo_gym varchar(250),
    @como_se_entero varchar(250),
    @observaciones text,
    @id_usuario int
)
AS
BEGIN
    DECLARE @hora_inscripcion time(0);
    SET @hora_inscripcion = CONVERT(time(0), GETDATE()); -- Convierte la hora actual a tipo time

    INSERT INTO Cliente (
        fechaInscripcion,
        horaInscripcion,
        fechaNacimiento,
        nombreApellido,
        genero,
        email,
        telefono,
        domicilio,
        dni,
        MotivoGym,
        ComoSeEntero,
        observaciones,
        idUsuario
    )
    VALUES (
        @fecha_inscripcion,
        @hora_inscripcion,
        @fecha_nacimiento,
        @nombre_apellido,
        @genero,
        @email,
        @telefono,
        @domicilio,
        @dni,
        @motivo_gym,
        @como_se_entero,
        @observaciones,
        @id_usuario
    );
END;