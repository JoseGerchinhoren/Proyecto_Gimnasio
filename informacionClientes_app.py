import streamlit as st
import pyodbc
import json
import pandas as pd

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Conexión a la base de datos SQL Server
db = pyodbc.connect(
    driver=config["driver"],
    server=config["server"],
    database=config["database"],
    uid=config["user"],
    pwd=config["password"]
)

def obtener_info_cliente(nombre_cliente):
    cursor = db.cursor()
    query = "SELECT * FROM Cliente WHERE nombreApellido = ?"
    cursor.execute(query, nombre_cliente)
    cliente_info = cursor.fetchone()
    cursor.close()
    return cliente_info

def obtener_nombres_clientes():
    cursor = db.cursor()
    query = "SELECT nombreApellido FROM Cliente"
    cursor.execute(query)
    nombres_clientes = [cliente[0] for cliente in cursor.fetchall()]
    cursor.close()
    return nombres_clientes

def obtener_pagos_cliente(id_cliente):
    cursor = db.cursor()
    query = """
    SELECT idCliente, idPago, fechaPago, montoPago, metodoPago, detallePago, idUsuario
    FROM Pago
    WHERE idCliente = ?
    ORDER BY idPago DESC
    """
    cursor.execute(query, id_cliente)
    pagos_cliente = cursor.fetchall()
    cursor.close()
    return pagos_cliente

def main():
    st.title("Información del Cliente")
    
    nombres_clientes = obtener_nombres_clientes()
    nombre_cliente_input = st.text_input("Ingrese el Nombre y Apellido del Cliente:")
    nombre_cliente = None
    
    if nombre_cliente_input:
        nombres_coincidentes = [nombre for nombre in nombres_clientes if nombre_cliente_input.lower() in nombre.lower()]
        if nombres_coincidentes:
            nombre_cliente = st.selectbox("Seleccione un nombre:", nombres_coincidentes)
    
    if nombre_cliente:
        cliente_info = obtener_info_cliente(nombre_cliente)
        if cliente_info:
            st.write("Información del Cliente:")
            st.write(f"ID del Cliente: {cliente_info[0]}")
            st.write(f"Nombre y Apellido: {cliente_info[4]}")
            st.write(f"Fecha de Inscripción: {cliente_info[1]}")
            st.write(f"Hora de Inscripción: {cliente_info[2]}")
            st.write(f"Fecha de Nacimiento: {cliente_info[3]}")
            st.write(f"Genero: {cliente_info[5]}")
            st.write(f"Email: {cliente_info[6]}")
            st.write(f"Teléfono: {cliente_info[7]}")
            st.write(f"Domicilio: {cliente_info[8]}")
            st.write(f"Número de DNI: {cliente_info[9]}")
            st.write(f"Requiere Instructor: {'Sí' if cliente_info[10] else 'No'}")
            st.write(f"Peso Inicial: {cliente_info[11]}")
            st.write(f"Objetivo: {cliente_info[12]}")
            st.write(f"Observaciones: {cliente_info[13]}")

            # Obtener el ID del cliente
            id_cliente = cliente_info[0]

            # Obtener los pagos del cliente
            pagos_cliente = obtener_pagos_cliente(id_cliente)

            if pagos_cliente:
                st.write("Pagos del Cliente, del más nuevo al más antiguo:")
                # Crear una lista de tuplas a partir de los datos de pagos_cliente
                pagos_data = [(p[0], p[1], p[2], p[3], p[4], p[5], p[6]) for p in pagos_cliente]
                # Crear el DataFrame con las columnas especificadas
                pagos_df = pd.DataFrame(pagos_data, columns=["idCliente", "idPago", "fechaPago", "montoPago", "metodoPago", "detallePago", "idUsuario"])
                st.dataframe(pagos_df)
            else:
                st.write("El cliente no tiene pagos registrados.")

        else:
            st.warning("Cliente no encontrado.")

if __name__ == "__main__":
    main()
