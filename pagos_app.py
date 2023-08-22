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

def guardar_pago(fecha_pago, id_cliente, nombre_apellido, monto_pago, metodo_pago, detalle_pago):
    cursor = db.cursor()
    query = "INSERT INTO Pagos (fechaPago, idCliente, nombreApellidoCliente, montoPago, metodoPago, detallePago) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (fecha_pago, id_cliente, nombre_apellido, monto_pago, metodo_pago, detalle_pago)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

def obtener_clientes():
    cursor = db.cursor()
    query = "SELECT idCliente, nombre_apellido FROM Clientes"
    cursor.execute(query)
    clientes = cursor.fetchall()
    cursor.close()
    return clientes

def main():
    st.title("Ingresar Pagos")
    
    fecha_pago = st.date_input("Fecha de Pago:")
    clientes = obtener_clientes()
    nombres_clientes = [cliente[1] for cliente in clientes]
    nombre_apellido = st.selectbox("Nombre y Apellido del Cliente:", nombres_clientes)
    
    id_cliente = [cliente[0] for cliente in clientes if cliente[1] == nombre_apellido][0]
    
    monto_pago = st.number_input("Monto del Pago:", min_value=0, format="%d")
    metodo_pago = st.text_input("Método de Pago:")
    detalle_pago = st.text_input("Detalle del Pago:")
    
    if st.button("Guardar Pago"):
        guardar_pago(fecha_pago, id_cliente, nombre_apellido, monto_pago, metodo_pago, detalle_pago)
        st.success("Pago guardado exitosamente!")
        st.experimental_rerun()

if __name__ == "__main__":
    main()
