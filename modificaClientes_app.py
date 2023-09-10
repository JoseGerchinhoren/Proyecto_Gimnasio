import streamlit as st
import pyodbc
import json

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Función para conectar a la base de datos
def conectar_bd():
    return pyodbc.connect(
        driver=config["driver"],
        server=config["server"],
        database=config["database"],
        uid=config["user"],
        pwd=config["password"]
    )

# Función para obtener los datos de un cliente por nombre y apellido
def obtener_datos_cliente(nombre_apellido):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    query = """
    SELECT *
    FROM Cliente
    WHERE nombreApellido = ?
    """
    
    cursor.execute(query, (nombre_apellido,))
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return row  # Devuelve una fila de datos del cliente o None si no se encuentra

# Función para obtener el ID de usuario a partir de su nombre y apellido
def obtener_id_usuario(nombre, apellido):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    query = """
    SELECT idUsuario
    FROM Usuario
    WHERE nombre = ? AND apellido = ?
    """
    
    cursor.execute(query, (nombre, apellido))
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return row[0] if row else None  # Devuelve el ID de usuario o None si no se encuentra

# Función para editar los datos de un cliente
def editar_cliente(id_cliente, campo_editar, nuevo_valor, id_usuario):
    if campo_editar == "idCliente":
        st.warning("El campo 'idCliente' no se puede editar.")
        return
    
    conn = conectar_bd()
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
    query_modificacion = """
    INSERT INTO ModificacionesClientes (idCliente, idUsuario, fechaModificacion)
    VALUES (?, ?, GETDATE())
    """
    values_modificacion = (id_cliente, id_usuario)
    cursor.execute(query_modificacion, values_modificacion)
    conn.commit()
    
    cursor.close()
    conn.close()

# Función para obtener los nombres de los clientes
def obtener_nombres_clientes():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    query = "SELECT nombreApellido FROM Cliente"
    cursor.execute(query)
    nombres_clientes = [cliente[0] for cliente in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return nombres_clientes

def main():
    st.title("Modificar Datos de Clientes")
    
    # Obtener nombre y apellido del usuario autenticado
    user_nombre_apellido = st.session_state.user_nombre_apellido

     # Obtener el ID de usuario a partir del nombre y apellido del usuario
    id_usuario = obtener_id_usuario(user_nombre_apellido)
    
    if id_usuario is not None:
        st.write("Modificar Clientes")
    
    st.write("Modificar Clientes")
    
    # Obtener la lista de nombres y apellidos de los clientes desde la base de datos
    nombres_clientes = obtener_nombres_clientes()
    
    # Crear un cuadro desplegable para seleccionar un cliente
    selected_cliente = st.selectbox("Seleccionar Cliente:", nombres_clientes)
    
    if selected_cliente:
        # Obtener los datos del cliente
        cliente_data = obtener_datos_cliente(selected_cliente)
        
        if cliente_data:
            st.write("Información del Cliente:")
            
            # Obtener el orden de los campos en la tabla "Cliente"
            campos_cliente = ["idCliente", "fechaInscripcion", "fechaNacimiento", "nombreApellido", "email", "telefono", "domicilio", "dni", "requiereInstructor", "pesoInicial", "objetivo", "observaciones"]
            
            # Texto amigable para mostrar los campos
            campos_amigables = {
                "idCliente": "ID de Cliente",
                "fechaInscripcion": "Fecha de Inscripción",
                "fechaNacimiento": "Fecha de Nacimiento",
                "nombreApellido": "Nombre y Apellido",
                "email": "Email",
                "telefono": "Teléfono",
                "domicilio": "Domicilio",
                "dni": "DNI",
                "requiereInstructor": "Requiere Instructor",
                "pesoInicial": "Peso Inicial",
                "objetivo": "Objetivo",
                "observaciones": "Observaciones"
            }
            
            # Iterar sobre los campos y sus valores
            for campo in campos_cliente:
                valor = cliente_data[campos_cliente.index(campo)]  # Valor del campo
                campo_amigable = campos_amigables.get(campo, campo)
                st.write(f"{campo_amigable}: {valor}")
            
            st.write("Editar Campos:")

            # Permitir al usuario seleccionar el campo a editar
            campo_editar = st.selectbox("Seleccione el campo a editar:", [campo for campo in campos_cliente if campo != "idCliente"])
            
            # Mostrar el valor actual en el campo de edición
            valor_actual = cliente_data[campos_cliente.index(campo_editar)]
            nuevo_valor = st.text_input(f"Nuevo valor de {campos_amigables.get(campo_editar, campo_editar)}:", valor_actual)
            
            if st.button("Guardar Cambios"):
                # Realizar la edición del campo seleccionado
                id_cliente = cliente_data.idCliente  # ID del cliente en la primera posición
                editar_cliente(id_cliente, campo_editar, nuevo_valor, id_usuario)
                st.success(f"Se ha editado el campo {campos_amigables.get(campo_editar, campo_editar)} correctamente.")
        else:
            st.error("Cliente no encontrado.")

if __name__ == "__main__":
    main()
