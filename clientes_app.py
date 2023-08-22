import streamlit as st
import mysql.connector
import json

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host=config["host"],
    user=config["user"],
    password=config["password"],
    database=config["database"]
)

def guardar_cliente(fecha_inscripcion, nombre_apellido, fecha_nacimiento, email, telefono, requiere_instructor, peso_inicial, objetivo, observaciones):
    cursor = db.cursor()
    query = "INSERT INTO Clientes (fecha_inscripcion, fecha_nacimiento, nombre_apellido, email, telefono, requiere_instructor, peso_inicial, objetivo, observaciones) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    nombre_apellido = nombre_apellido.strip()  # Eliminar posibles espacios al inicio y final
    nombre, apellido = nombre_apellido.rsplit(maxsplit=1)
    values = (fecha_inscripcion, fecha_nacimiento, nombre_apellido, email, telefono, requiere_instructor, peso_inicial, objetivo, observaciones)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

def main():
    st.title("Ingresar Datos de Clientes")
    
    fecha_inscripcion = st.date_input("Fecha de Inscripción:")
    nombre_apellido = st.text_input("Nombre/s y Apellido/s del Cliente:")
    fecha_nacimiento = st.date_input("Fecha de Nacimiento:")
    email = st.text_input("Email:")
    telefono = st.text_input("Número de Teléfono Celular:")
    requiere_instructor = st.checkbox("Requiere Instructor")
    peso_inicial = st.number_input("Peso Inicial:", step=1, format="%d")
    objetivo_options = ["Sin especificar", "Bajar de Peso", "Subir de Peso", "Mantener"]
    objetivo = st.selectbox("Objetivo:", objetivo_options)
    observaciones = st.text_area("Observaciones")
    
    if st.button("Guardar Cliente"):
        guardar_cliente(fecha_inscripcion, nombre_apellido, fecha_nacimiento, email, telefono, requiere_instructor, peso_inicial, objetivo, observaciones)
        st.success(f"Cliente {nombre_apellido} guardado exitosamente!")

if __name__ == "__main__":
    main()
