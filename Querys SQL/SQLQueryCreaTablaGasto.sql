CREATE TABLE Gasto (
    idGasto INT PRIMARY KEY IDENTITY(1,1),
    fecha DATE,
    motivo VARCHAR(255) NOT NULL,
    lugar VARCHAR(255) NOT NULL,
    monto INT NOT NULL,
    metodoPago VARCHAR(50) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    observacion VARCHAR(500) NOT NULL,  -- Puedes ajustar la longitud máxima según tus necesidades

    -- Almacenamiento de ruta de archivo en el sistema de archivos
    rutaArchivo VARCHAR(255),  -- Ajusta la longitud según tus necesidades

    -- Almacenamiento de archivo como datos binarios
    archivo VARBINARY(MAX)
);