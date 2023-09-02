import streamlit as st
import pyodbc
import json
from datetime import datetime

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Función para establecer la conexión a la base de datos
def conectar_db():
    return pyodbc.connect(
        driver=config["driver"],
        server=config["server"],
        database=config["database"],
        uid=config["user"],
        pwd=config["password"]
    )

# Función para obtener los datos de un cliente por su ID
def obtener_datos_cliente(id_cliente):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = """
    SELECT * FROM Cliente
    WHERE idCliente = ?
    """
    
    cursor.execute(query, (id_cliente,))
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return row  # Devuelve una fila de datos del cliente o None si no se encuentra

# Función para obtener los pagos de un cliente por su ID
def obtener_pagos_cliente(id_cliente):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = """
    SELECT * FROM Pago
    WHERE idCliente = ?
    """
    
    cursor.execute(query, (id_cliente,))
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return rows  # Devuelve una lista de filas de datos de pagos del cliente

# Función para editar un pago por su ID
def editar_pago(id_pago, fecha_pago, monto, metodo_pago, detalle_pago):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = """
    UPDATE Pago
    SET
        fecha_pago = ?,
        monto = ?,
        metodoPago = ?,
        detallePago = ?
    WHERE idPago = ?
    """
    
    values = (fecha_pago, monto, metodo_pago, detalle_pago, id_pago)
    cursor.execute(query, values)
    conn.commit()
    
    # Registrar la modificación en la tabla ModificacionesPagos
    usuario_modificacion = st.session_state.user_nombre_apellido  # Nombre y apellido del usuario que realiza la modificación
    query_modificacion = """
    INSERT INTO ModificacionesPagos (idPago, usuarioModificacion, fecha_modificacion)
    VALUES (?, ?, GETDATE())
    """
    values_modificacion = (id_pago, usuario_modificacion)
    cursor.execute(query_modificacion, values_modificacion)
    conn.commit()
    
    cursor.close()
    conn.close()

# Función para obtener los datos de un pago por su ID
def obtener_datos_pago(id_pago):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = """
    SELECT * FROM Pago
    WHERE idPago = ?
    """
    
    cursor.execute(query, (id_pago,))
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return row  # Devuelve una fila de datos del pago o None si no se encuentra

def main():
    st.title("Modificar Pagos de Clientes")
    
    # Obtener nombre y apellido del usuario autenticado
    user_nombre_apellido = st.session_state.user_nombre_apellido
    
    st.write("Modificar Pagos")
    
    # Obtener la lista de nombres y apellidos de los clientes desde la base de datos
    conn = conectar_db()
    cursor = conn.cursor()
    
    query_clientes = "SELECT idCliente, nombre_apellido FROM Cliente"
    cursor.execute(query_clientes)
    clientes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    # Crear un cuadro desplegable para seleccionar un cliente
    selected_cliente = st.selectbox("Seleccionar Cliente:", clientes, format_func=lambda x: x[1])
    
    if selected_cliente:
        id_cliente = selected_cliente[0]
        nombre_cliente = selected_cliente[1]
        
        # Obtener los pagos del cliente
        pagos_cliente = obtener_pagos_cliente(id_cliente)
        
        if pagos_cliente:
            st.write(f"Pagos de {nombre_cliente}:")
            
            # Mostrar los pagos del cliente en una tabla
            st.write(pagos_cliente)
            
            # Permitir al usuario seleccionar un pago para editar por su ID
            id_pago = st.number_input("ID del Pago a Editar", min_value=1)
            
            if id_pago:
                # Verificar si el ID del pago ingresado pertenece al cliente
                if any(pago[0] == id_pago for pago in pagos_cliente):
                    st.write("Información del Pago:")
                    
                    # Obtener los datos del pago
                    pago_data = obtener_datos_pago(id_pago)
                    
                    # Iterar sobre los campos y sus valores
                    for i in range(len(pago_data.cursor_description)):
                        campo = pago_data.cursor_description[i][0]  # Nombre del campo desde el cursor
                        valor = pago_data[i]  # Valor del campo
                        
                        # Mostrar cada campo y su valor en una fila
                        st.write(f"{campo}: {valor}")
                    
                    # Permitir al usuario editar los campos del pago
                    fecha_pago = st.date_input("Fecha de Pago", value=datetime.strptime(pago_data[2], "%Y-%m-%d"))
                    monto = st.number_input("Monto", value=pago_data[3])
                    metodo_pago = st.text_input("Método de Pago", value=pago_data[4])
                    detalle_pago = st.text_area("Detalle de Pago", value=pago_data[5])
                    
                    if st.button("Guardar Cambios"):
                        # Realizar la edición del pago con los nuevos valores
                        editar_pago(id_pago, fecha_pago, monto, metodo_pago, detalle_pago)
                        st.success("Se ha editado el pago correctamente.")
                else:
                    st.error("ID de Pago no válido para este cliente.")
            else:
                st.warning("Ingrese un ID de Pago válido para editar.")
        else:
            st.warning(f"No se encontraron pagos para {nombre_cliente}.")
    
if __name__ == "__main__":
    main()
