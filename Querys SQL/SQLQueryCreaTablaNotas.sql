USE SixGym;

CREATE TABLE Notas (
    idNota INT PRIMARY KEY IDENTITY(1,1),
    idUsuario INT,
    fecha DATE,
    nota TEXT
);