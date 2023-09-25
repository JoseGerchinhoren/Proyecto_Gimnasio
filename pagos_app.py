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

# Función para obtener el ID de usuario a partir de su nombre y apellido
def obtener_id_usuario(nombre, apellido):
    cursor = db.cursor()
    query = """
    SELECT idUsuario
    FROM Usuario
    WHERE nombre = ? AND apellido = ?
    """
    cursor.execute(query, (nombre, apellido))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None  # Devuelve el ID de usuario o None si no se encuentra

def guardar_pago(fecha_pago, id_cliente, monto_pago, metodo_pago, detalle_pago, id_usuario):
    cursor = db.cursor()
    
    try:
        # Llamar al stored procedure para insertar el pago
        cursor.execute("EXEC InsertarPago ?, ?, ?, ?, ?, ?", fecha_pago, id_cliente, monto_pago, metodo_pago, detalle_pago, id_usuario)
        db.commit()
        st.success("Pago guardado exitosamente!")
    except pyodbc.Error as e:
        db.rollback()
        st.error(f"Error al guardar el pago: {str(e)}")
    finally:
        cursor.close()
    
def obtener_clientes():
    cursor = db.cursor()
    query = "SELECT idCliente, nombreApellido FROM Cliente"
    cursor.execute(query)
    clientes = cursor.fetchall()
    cursor.close()
    return clientes

def main():
    st.title("Ingresar Pagos")
    
    fecha_pago = st.date_input("Fecha de Pago:", key="fecha_pago")
    
    nombre_apellido_input = st.text_input("Nombre y Apellido del Cliente:", key="nombre_apellido")
    nombre_apellido = None
    
    # Obtener el nombre y apellido del usuario autenticado desde la variable de sesión
    nombre_usuario_actual = st.session_state.user_nombre_apellido
    
    if nombre_apellido_input:
        nombres_clientes = [cliente[1] for cliente in obtener_clientes()]
        nombres_coincidentes = [nombre for nombre in nombres_clientes if nombre_apellido_input.lower() in nombre.lower()]
        if nombres_coincidentes:
            nombre_apellido = st.selectbox("Seleccione un nombre:", nombres_coincidentes, key="nombre_apellido_select")
    
    id_cliente = None
    if nombre_apellido:
        id_cliente = [cliente[0] for cliente in obtener_clientes() if cliente[1] == nombre_apellido][0]
    
    monto_pago = st.number_input("Monto del Pago:", min_value=0, format="%d", key="monto_pago")
    # Campo de método de pago como un desplegable
    metodo_pago_options = ["Efectivo", "Transferencia", "Tarjeta de Crédito", "Tarjeta de Débito", "Otro"]
    metodo_pago = st.selectbox("Método de Pago:", metodo_pago_options, key="metodo_pago")
    
    detalle_pago = st.text_input("Detalle del Pago:", key="detalle_pago")
    
    if st.button("Guardar Pago"):
        if id_cliente:
            # Obtén el nombre y apellido del usuario actual y luego el idUsuario
            usuario_actual_nombre_apellido = st.session_state.user_nombre_apellido
            nombre_usuario_actual = usuario_actual_nombre_apellido.split()
            
            if len(nombre_usuario_actual) == 2:
                nombre_usuario = nombre_usuario_actual[0]
                apellido_usuario = nombre_usuario_actual[1]
                id_usuario = obtener_id_usuario(nombre_usuario, apellido_usuario)
                
                if id_usuario:
                    guardar_pago(fecha_pago, id_cliente, monto_pago, metodo_pago, detalle_pago, id_usuario)
                else:
                    st.warning("No se pudo obtener el ID de usuario.")
            else:
                st.warning("El nombre y apellido del usuario actual no se pueden determinar.")
        else:
            st.warning("Seleccione un nombre de cliente válido antes de guardar el pago.")

if __name__ == "__main__":
    main()
