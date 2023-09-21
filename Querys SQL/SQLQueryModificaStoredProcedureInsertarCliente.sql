USE [SixGym]
GO
/****** Object:  StoredProcedure [dbo].[InsertarCliente]    Script Date: 21/9/2023 02:24:41 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
ALTER PROCEDURE [dbo].[InsertarCliente] (
    @fecha_inscripcion datetime,
    @fecha_nacimiento date,
    @nombre_apellido varchar(255),
	@genero varchar(50),
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
        requiereInstructor,
        pesoInicial,
        objetivo,
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
        @requiere_instructor,
        @peso_inicial,
        @objetivo,
        @observaciones,
        @id_usuario
    );
END;