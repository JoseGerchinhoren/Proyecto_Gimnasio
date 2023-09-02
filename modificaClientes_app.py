import streamlit as st
import pyodbc
import json

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Función para obtener los datos de un cliente por nombre y apellido
def obtener_datos_cliente(nombre_apellido):
    conn = pyodbc.connect(
        driver=config["driver"],
        server=config["server"],
        database=config["database"],
        uid=config["user"],
        pwd=config["password"]
    )
    cursor = conn.cursor()
    
    query = """
    SELECT * FROM Cliente
    WHERE nombre_apellido = ?
    """
    
    cursor.execute(query, (nombre_apellido,))
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return row  # Devuelve una fila de datos del cliente o None si no se encuentra

# Función para editar los datos de un cliente
def editar_cliente(id_cliente, campo_editar, nuevo_valor):
    if campo_editar == "idCliente":
        st.warning("El campo 'idCliente' no se puede editar.")
        return
    
    conn = pyodbc.connect(
        driver=config["driver"],
        server=config["server"],
        database=config["database"],
        uid=config["user"],
        pwd=config["password"]
    )
    cursor = conn.cursor()
    
    query = f"""
    UPDATE Cliente
    SET {campo_editar} = ?
    WHERE idCliente = ?
    """
    
    values = (nuevo_valor, id_cliente)
    cursor.execute(query, values)
    conn.commit()
    
    # Registrar la modificación en la tabla ModificacionesClientes
    usuario_modificacion = st.session_state.user_nombre_apellido  # Nombre y apellido del usuario que realiza la modificación
    query_modificacion = """
    INSERT INTO ModificacionesClientes (idCliente, usuarioModificacion, fechaModificacion)
    VALUES (?, ?, GETDATE())
    """
    values_modificacion = (id_cliente, usuario_modificacion)
    cursor.execute(query_modificacion, values_modificacion)
    conn.commit()
    
    cursor.close()
    conn.close()

# Función para obtener los nombres de los clientes
def obtener_nombres_clientes():
    conn = pyodbc.connect(
        driver=config["driver"],
        server=config["server"],
        database=config["database"],
        uid=config["user"],
        pwd=config["password"]
    )
    cursor = conn.cursor()
    
    query = "SELECT nombre_apellido FROM Cliente"
    cursor.execute(query)
    nombres_clientes = [cliente[0] for cliente in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return nombres_clientes

def main():
    st.title("Modificar Datos de Clientes")
    
    # Obtener nombre y apellido del cliente para editar
    nombre_apellido = st.selectbox("Seleccione un Cliente:", obtener_nombres_clientes())
    
    if nombre_apellido:
        # Obtener los datos del cliente
        cliente_data = obtener_datos_cliente(nombre_apellido)
        
        if cliente_data:
            st.write("Información del Cliente:")
            
            # Iterar sobre los campos y sus valores
            for i in range(len(cliente_data.cursor_description)):
                campo = cliente_data.cursor_description[i][0]  # Nombre del campo desde el cursor
                valor = cliente_data[i]  # Valor del campo
                
                # Mostrar cada campo y su valor en una fila
                st.write(f"{campo}: {valor}")
            
            # Permitir al usuario seleccionar el campo a editar
            campos_editables = [campo[0] for campo in cliente_data.cursor_description if campo[0] != "idCliente"]
            campo_editar = st.selectbox("Seleccione el campo a editar:", campos_editables)
            
            # Permitir al usuario editar el campo
            nuevo_valor = st.text_input(f"Nuevo valor de {campo_editar}:", cliente_data[campos_editables.index(campo_editar)])
            
            if st.button("Guardar Cambios"):
                # Realizar la edición del campo seleccionado
                id_cliente = cliente_data.idCliente  # ID del cliente en la primera posición
                editar_cliente(id_cliente, campo_editar, nuevo_valor)
                st.success(f"Se ha editado el campo {campo_editar} correctamente.")
        else:
            st.error("Cliente no encontrado.")
    
if __name__ == "__main__":
    main()