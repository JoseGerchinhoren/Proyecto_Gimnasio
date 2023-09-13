CREATE TABLE Gasto (
    idGasto INT PRIMARY KEY IDENTITY(1,1),
    fecha DATE,
    motivo NVARCHAR(255) NOT NULL,
    lugar NVARCHAR(255) NOT NULL,
    monto INT NOT NULL,
    metodoPago NVARCHAR(50) NOT NULL,
    categoria NVARCHAR(50) NOT NULL,
    observacion NVARCHAR(500) NOT NULL,  -- Puedes ajustar la longitud máxima según tus necesidades

    -- Almacenamiento de ruta de archivo en el sistema de archivos
    rutaArchivo NVARCHAR(255),  -- Ajusta la longitud según tus necesidades

    -- Almacenamiento de archivo como datos binarios
    archivo VARBINARY(MAX)
);