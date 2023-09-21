import streamlit as st
import pyodbc
import json
from datetime import datetime

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Conexión a la base de datos SQL Server
conn = pyodbc.connect(
    driver=config["driver"],
    server=config["server"],
    database=config["database"],
    uid=config["user"],
    pwd=config["password"]
)

# Función para obtener el ID de usuario a partir de su nombre y apellido
def obtener_id_usuario(nombre, apellido):
    cursor = conn.cursor()
    
    query = """
    SELECT idUsuario
    FROM Usuario
    WHERE nombre = ? AND apellido = ?
    """
    
    cursor.execute(query, (nombre, apellido))
    row = cursor.fetchone()
    
    cursor.close()
    
    return row[0] if row else None  # Devuelve el ID de usuario o None si no se encuentra

def guardar_cliente(fecha_inscripcion, fecha_nacimiento, nombre_apellido, genero, email, telefono, domicilio, dni, requiere_instructor, peso_inicial, objetivo, observaciones, idUsuario):
    cursor = conn.cursor()
    
    # Obtener el ID de usuario a partir del nombre y apellido del usuario
    nombre, apellido = idUsuario.split(" ")  # Divide el nombre y el apellido
    id_usuario = obtener_id_usuario(nombre, apellido)

    # Ejecutar el stored procedure con los parámetros requeridos
    cursor.execute("EXEC InsertarCliente ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
                   (fecha_inscripcion, fecha_nacimiento, nombre_apellido, genero, email, telefono, domicilio, dni, requiere_instructor, peso_inicial, objetivo, observaciones, id_usuario))
    
    conn.commit()
    cursor.close()

def main():
    st.title("Ingresar Datos de Clientes")
    
    fecha_inscripcion = st.date_input("Fecha de Inscripción:") 
    nombre_apellido = st.text_input("Nombre/s y Apellido/s del Cliente:")
    fecha_nacimiento = st.date_input("Fecha de Nacimiento:")
    genero_options = ["Masculino", "Femenino", "Otro"]
    genero = st.selectbox("Genero:", genero_options)
    email = st.text_input("Email:")
    telefono = st.text_input("Número de Teléfono Celular:")
    domicilio = st.text_input("Domicilio:")
    dni = st.text_input("Número de DNI:")
    requiere_instructor = st.checkbox("Requiere Instructor")
    peso_inicial = st.number_input("Peso Inicial:", step=1, format="%d")
    objetivo_options = ["Sin especificar", "Bajar de Peso", "Subir de Peso", "Mantener"]
    objetivo = st.selectbox("Objetivo:", objetivo_options)
    observaciones = st.text_area("Observaciones")
    
    # Obtener el nombre y apellido del usuario autenticado
    idUsuario = st.session_state.get("user_nombre_apellido", "")
    
    if st.button("Guardar Cliente"):
        guardar_cliente(fecha_inscripcion, fecha_nacimiento, nombre_apellido, genero, email, telefono, domicilio, dni, requiere_instructor, peso_inicial, objetivo, observaciones, idUsuario)
        st.success(f"Cliente {nombre_apellido} guardado exitosamente!")

if __name__ == "__main__":
    main()
