CREATE TABLE Usuario (
    idUsuario INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    fechaNacimiento DATE,
    dni VARCHAR(15) NOT NULL UNIQUE,
    domicilio VARCHAR(255),
    fechaCreacion DATETIME NOT NULL DEFAULT GETDATE(),
    puesto VARCHAR(50) NOT NULL,
    rol VARCHAR(50) NOT NULL
);