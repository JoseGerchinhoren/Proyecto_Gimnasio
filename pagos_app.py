import streamlit as st
import pyodbc
import json

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

def guardar_pago(fecha_pago, id_cliente, nombre_apellido, monto_pago, metodo_pago, detalle_pago):
    cursor = db.cursor()
    query = "INSERT INTO Pago (fechaPago, idCliente, nombreApellidoCliente, montoPago, metodoPago, detallePago) VALUES (?, ?, ?, ?, ?, ?)"
    values = (fecha_pago, id_cliente, nombre_apellido, monto_pago, metodo_pago, detalle_pago)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

def obtener_clientes():
    cursor = db.cursor()
    query = "SELECT idCliente, nombre_apellido FROM Cliente"
    cursor.execute(query)
    clientes = cursor.fetchall()
    cursor.close()
    return clientes

def main():
    st.title("Ingresar Pagos")
    
    fecha_pago = st.date_input("Fecha de Pago:", key="fecha_pago")
    
    nombre_apellido_input = st.text_input("Nombre y Apellido del Cliente:", key="nombre_apellido")
    nombre_apellido = None
    if nombre_apellido_input:
        nombres_clientes = [cliente[1] for cliente in obtener_clientes()]
        nombres_coincidentes = [nombre for nombre in nombres_clientes if nombre_apellido_input.lower() in nombre.lower()]
        if nombres_coincidentes:
            nombre_apellido = st.selectbox("Seleccione un nombre:", nombres_coincidentes, key="nombre_apellido_select")
    
    id_cliente = None
    if nombre_apellido:
        id_cliente = [cliente[0] for cliente in obtener_clientes() if cliente[1] == nombre_apellido][0]
    
    monto_pago = st.number_input("Monto del Pago:", min_value=0, format="%d", key="monto_pago")
    metodo_pago = st.text_input("Método de Pago:", key="metodo_pago")
    detalle_pago = st.text_input("Detalle del Pago:", key="detalle_pago")
    
    if st.button("Guardar Pago"):
        if id_cliente:
            guardar_pago(fecha_pago, id_cliente, nombre_apellido, monto_pago, metodo_pago, detalle_pago)
            st.success("Pago guardado exitosamente!")
        else:
            st.warning("Seleccione un nombre de cliente válido antes de guardar el pago.")

if __name__ == "__main__":
    main()
