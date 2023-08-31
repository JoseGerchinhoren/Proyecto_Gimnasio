import streamlit as st
import pyodbc
import json

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

def guardar_cliente(fecha_inscripcion, nombre_apellido, fecha_nacimiento, email, telefono, domicilio, dni, requiere_instructor, peso_inicial, objetivo, observaciones):
    cursor = conn.cursor()
    query = "INSERT INTO Cliente (fecha_inscripcion, fecha_nacimiento, nombre_apellido, email, telefono, domicilio, dni, requiere_instructor, peso_inicial, objetivo, observaciones) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    nombre_apellido = nombre_apellido.strip()  # Eliminar posibles espacios al inicio y final
    nombre, apellido = nombre_apellido.rsplit(maxsplit=1)
    values = (fecha_inscripcion, fecha_nacimiento, nombre_apellido, email, telefono, domicilio, dni, requiere_instructor, peso_inicial, objetivo, observaciones)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()

def main():
    st.title("Ingresar Datos de Clientes")
    
    fecha_inscripcion = st.date_input("Fecha de Inscripción:")
    nombre_apellido = st.text_input("Nombre/s y Apellido/s del Cliente:")
    fecha_nacimiento = st.date_input("Fecha de Nacimiento:")
    email = st.text_input("Email:")
    telefono = st.text_input("Número de Teléfono Celular:")
    domicilio = st.text_input("Domicilio:")
    dni = st.text_input("Número de DNI:")
    requiere_instructor = st.checkbox("Requiere Instructor")
    peso_inicial = st.number_input("Peso Inicial:", step=1, format="%d")
    objetivo_options = ["Sin especificar", "Bajar de Peso", "Subir de Peso", "Mantener"]
    objetivo = st.selectbox("Objetivo:", objetivo_options)
    observaciones = st.text_area("Observaciones")
    
    if st.button("Guardar Cliente"):
        guardar_cliente(fecha_inscripcion, nombre_apellido, fecha_nacimiento, email, telefono, domicilio, dni, requiere_instructor, peso_inicial, objetivo, observaciones)
        st.success(f"Cliente {nombre_apellido} guardado exitosamente!")

if __name__ == "__main__":
    main()