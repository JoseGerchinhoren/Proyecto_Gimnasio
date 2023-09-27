import streamlit as st
import pyodbc
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

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

def calcular_estado_cuota(ultima_fecha_pago, fecha_actual):
    if ultima_fecha_pago:
        diferencia_meses = (fecha_actual.year - ultima_fecha_pago.year) * 12 + (fecha_actual.month - ultima_fecha_pago.month)
    else:
        diferencia_meses = None

    if diferencia_meses is None:
        estado_texto = "Sin pagos registrados"
        estado_color = "gray"
    elif diferencia_meses >= 1:
        estado_texto = "Cuota vencida"
        estado_color = "red"
    else:
        estado_texto = "Cuota al día"
        estado_color = "green"

    return estado_texto, estado_color

def quitar_marco(fig, ax):
    # Eliminar los bordes de la figura
    fig.patch.set_facecolor('white')
    ax.set_frame_on(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False)

    # Eliminar los márgenes del eje x y del eje y
    ax.margins(0, 0)

    return fig, ax

def main():
    st.title("Información del Cliente")
    st.title("Buscar Cliente")
    
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
            st.title("Estado de Cuota del Cliente")
            # Obtener el ID del cliente
            id_cliente = cliente_info[0]

            # Obtener los pagos del cliente
            pagos_cliente = obtener_pagos_cliente(id_cliente)
            
            # Obtener la figura y la caja de ejes
            fig, ax = plt.subplots(figsize=(4, 1))

            # Calcular el estado de la cuota
            estado_texto, estado_color = calcular_estado_cuota(pagos_cliente[0][2] if pagos_cliente else None, datetime.now())

            # Agregar el texto y el sector de estado
            ax.bar([1], [1], color=estado_color)
            ax.text(1, 0.5, estado_texto, ha='center', va='center', fontsize=16, color='white')
            ax.set_xticks([])
            ax.set_yticks([])

            # Quitar el marco
            fig, ax = quitar_marco(fig, ax)

            # Mostrar el gráfico
            st.pyplot(fig, use_container_width=True, bbox_inches='tight', pad_inches=0)

            st.title("Pagos del Cliente")
            
            if pagos_cliente:
                st.write("Ordenados del más nuevo al más antiguo:")
                # Crear una lista de tuplas a partir de los datos de pagos_cliente
                pagos_data = [(p[0], p[1], p[2], p[3], p[4], p[5], p[6]) for p in pagos_cliente]
                # Crear el DataFrame con las columnas especificadas
                pagos_df = pd.DataFrame(pagos_data, columns=["idCliente", "idPago", "fechaPago", "montoPago", "metodoPago", "detallePago", "idUsuario"])
                st.dataframe(pagos_df)
            else:
                st.write("El cliente no tiene pagos registrados.")
            
            st.title("Información del Cliente")
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

        else:
            st.warning("Cliente no encontrado.")

if __name__ == "__main__":
    main()
