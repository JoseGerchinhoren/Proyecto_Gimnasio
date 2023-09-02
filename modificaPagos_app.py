import streamlit as st
import pyodbc
import json

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Función para editar los pagos de un cliente
def editar_pago(id_pago, id_cliente, fecha_pago, monto):
    conn = pyodbc.connect(
        driver=config["driver"],
        server=config["server"],
        database=config["database"],
        uid=config["user"],
        pwd=config["password"]
    )
    cursor = conn.cursor()
    
    query = """
    UPDATE Pago
    SET
        idCliente = ?,
        fecha_pago = ?,
        monto = ?
    WHERE idPago = ?
    """
    
    values = (id_cliente, fecha_pago, monto, id_pago)
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

def main():
    st.title("Modificar Pagos de Clientes")
    
    # Obtener nombre y apellido del usuario autenticado
    user_nombre_apellido = st.session_state.user_nombre_apellido
    
    st.write("Modificar Pagos")
    # Aquí puedes agregar los campos y la lógica para modificar pagos de clientes

if __name__ == "__main__":
    main()
