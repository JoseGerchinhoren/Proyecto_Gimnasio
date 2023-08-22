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

def obtener_info_cliente(nombre_cliente):
    cursor = db.cursor()
    query = "SELECT * FROM Clientes WHERE nombre_apellido = %s"
    cursor.execute(query, (nombre_cliente,))
    cliente_info = cursor.fetchone()
    cursor.close()
    return cliente_info

def main():
    st.title("Información del Cliente")

    nombre_cliente = st.text_input("Ingrese el Nombre y Apellido del Cliente:")
    
    if nombre_cliente:
        cliente_info = obtener_info_cliente(nombre_cliente)
        if cliente_info:
            st.write("Información del Cliente:")
            st.write(f"Nombre: {cliente_info[3]} {cliente_info[4]}")
            st.write(f"Fecha de Inscripción: {cliente_info[1]}")
            st.write(f"Fecha de Nacimiento: {cliente_info[2]}")
            st.write(f"Email: {cliente_info[5]}")
            st.write(f"Teléfono: {cliente_info[6]}")
            st.write(f"Requiere Instructor: {'Sí' if cliente_info[7] else 'No'}")
            st.write(f"Peso Inicial: {cliente_info[8]}")
            st.write(f"Objetivo: {cliente_info[9]}")
            st.write(f"Observaciones: {cliente_info[10]}")
        else:
            st.warning("Cliente no encontrado.")

if __name__ == "__main__":
    main()
