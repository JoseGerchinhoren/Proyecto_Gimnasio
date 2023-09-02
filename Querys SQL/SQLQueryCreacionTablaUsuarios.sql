CREATE TABLE Usuario (
    idUsuario INT PRIMARY KEY IDENTITY(1,1),
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    contraseña VARCHAR(255) NOT NULL,
    fecha_nacimiento DATE,
    dni VARCHAR(15) NOT NULL UNIQUE,
    domicilio VARCHAR(255),
    fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
    puesto VARCHAR(50) CHECK (puesto IN ('personal_atencion_publico', 'personal_gestion', 'jefe')) NOT NULL,
    rol VARCHAR(50) CHECK (rol IN ('admin', 'usuario')) NOT NULL
);