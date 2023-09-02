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

def guardar_usuario(nombre, apellido, email, contraseña, fecha_nacimiento, dni, domicilio, puesto, rol):
    cursor = conn.cursor()
    query = "INSERT INTO Usuario (nombre, apellido, email, contraseña, fecha_nacimiento, dni, domicilio, puesto, rol) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
    values = (nombre, apellido, email, contraseña, fecha_nacimiento, dni, domicilio, puesto, rol)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()

def main():
    st.title("Ingresar Datos de Usuarios")
    
    nombre = st.text_input("Nombre:")
    apellido = st.text_input("Apellido:")
    email = st.text_input("Email:")
    contraseña = st.text_input("Contraseña:", type="password")
    confirmar_contraseña = st.text_input("Confirmar Contraseña:", type="password")
    fecha_nacimiento = st.date_input("Fecha de Nacimiento:")
    dni = st.text_input("Número de DNI:")
    domicilio = st.text_input("Domicilio:")
    puesto_options = ["personal_atencion_publico", "personal_gestion", "jefe"]
    puesto = st.selectbox("Puesto:", puesto_options)
    rol_options = ["admin", "usuario"]
    rol = st.selectbox("Rol:", rol_options)
    
    if st.button("Guardar Usuario"):
        if contraseña == confirmar_contraseña:
            guardar_usuario(nombre, apellido, email, contraseña, fecha_nacimiento, dni, domicilio, puesto, rol)
            st.success(f"Usuario {nombre} {apellido} guardado exitosamente!")
        else:
            st.error("Las contraseñas no coinciden. Vuelve a intentarlo.")

