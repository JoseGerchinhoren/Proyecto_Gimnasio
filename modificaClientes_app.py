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

# Función para obtener los datos de un cliente por nombre y apellido
def obtener_datos_cliente(nombre_apellido):
    cursor = db.cursor()
    query = """
    SELECT * FROM Cliente
    WHERE nombreApellido = ?
    """
    cursor.execute(query, (nombre_apellido,))
    row = cursor.fetchone()
    cursor.close()
    return row  # Devuelve una fila de datos del cliente o None si no se encuentra

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

# Función para editar los datos de un cliente
def editar_cliente(id_cliente, campo_editar, nuevo_valor, nombre_usuario, campo_modificado):
    if campo_editar == "idCliente":
        st.warning("El campo 'idCliente' no se puede editar.")
        return
    
    cursor = db.cursor()
    
    # Obtener el valor anterior del campo editado
    query_valor_anterior = f"""
    SELECT {campo_editar}
    FROM Cliente
    WHERE idCliente = ?
    """
    cursor.execute(query_valor_anterior, (id_cliente,))
    valor_anterior = cursor.fetchone()[0]
    
    # Realizar la actualización en la tabla Cliente
    query = f"""
    UPDATE Cliente
    SET {campo_editar} = ?
    WHERE idCliente = ?
    """
    values = (nuevo_valor, id_cliente)
    cursor.execute(query, values)
    db.commit()
    
    # Obtener el ID de usuario a partir del nombre y apellido del usuario
    nombre, apellido = nombre_usuario.split(" ")  # Divide el nombre y el apellido
    id_usuario_modificacion = obtener_id_usuario(nombre, apellido)

    # Registrar la modificación en la tabla ModificacionesClientes
    query_modificacion = """
    INSERT INTO ModificacionesClientes (idCliente, idUsuario, fechaModificacion, campoModificado, valorAnterior)
    VALUES (?, ?, GETDATE(), ?, ?)
    """
    values_modificacion = (id_cliente, id_usuario_modificacion, campo_modificado, valor_anterior)
    cursor.execute(query_modificacion, values_modificacion)
    db.commit()
    
    cursor.close()

# Función para obtener los nombres de los clientes
def obtener_nombres_clientes():
    cursor = db.cursor()
    
    query = "SELECT nombreApellido FROM Cliente"
    cursor.execute(query)
    nombres_clientes = [cliente[0] for cliente in cursor.fetchall()]
    
    cursor.close()
    
    return nombres_clientes

# Función para eliminar un cliente por ID
def eliminar_cliente(id_cliente, nombre_cliente):
    cursor = db.cursor()

    try:
        # Eliminar el cliente de la tabla Cliente
        query_eliminar_cliente = """
        DELETE FROM Cliente WHERE idCliente = ?
        """
    
        cursor.execute(query_eliminar_cliente, (id_cliente,))
    
        db.commit()
        st.success(f"Se ha eliminado el cliente '{nombre_cliente}' correctamente.")
    except pyodbc.IntegrityError as e:
        st.error(f"No se puede eliminar el cliente '{nombre_cliente}' debido a restricciones de integridad en la base de datos. Asegúrese de que no existan registros relacionados en otras tablas.")
    except Exception as e:
        st.error(f"Se produjo un error al eliminar el cliente '{nombre_cliente}': {str(e)}")
    finally:
        cursor.close()

def main():
    st.title("Modificar Datos de Clientes")

    nombres_clientes = obtener_nombres_clientes()
    nombre_cliente_input = st.text_input("Ingrese el Nombre y Apellido del Cliente:")
    nombre_cliente = None

    if nombre_cliente_input:
        nombres_coincidentes = [nombre for nombre in nombres_clientes if nombre_cliente_input.lower() in nombre.lower()]
        if nombres_coincidentes:
            nombre_cliente = st.selectbox("Seleccione un nombre:", nombres_coincidentes)

    if nombre_cliente:
        # Obtener los datos del cliente
        cliente_data = obtener_datos_cliente(nombre_cliente)
        
        if cliente_data:
            st.write("Información del Cliente:")
            
            # Obtener el orden de los campos en la tabla "Cliente"
            campos_cliente = ["idCliente", "fechaInscripcion", "horaInscripcion", "fechaNacimiento", "nombreApellido", "genero","email", "telefono", "domicilio", "dni", "requiereInstructor", "pesoInicial", "objetivo", "observaciones"]
            
            # Texto amigable para mostrar los campos
            campos_amigables = {
                "idCliente": "ID de Cliente",
                "fechaInscripcion": "Fecha de Inscripción",
                "horaInscripcion": "Hora de Inscripción",
                "fechaNacimiento": "Fecha de Nacimiento",
                "nombreApellido": "Nombre y Apellido",
                "genero": "Genero",
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
                usuario_modificacion = st.session_state.user_nombre_apellido  # Nombre y apellido del usuario que realiza la modificación
                campo_modificado = campo_editar  # Nombre del campo modificado
                editar_cliente(id_cliente, campo_editar, nuevo_valor, usuario_modificacion, campo_modificado)
                st.success(f"Se ha editado el campo {campos_amigables.get(campo_editar, campo_editar)} correctamente.")
            
            # Agregar un botón para eliminar al cliente
            if st.button("Eliminar Cliente"):
                eliminar_cliente(cliente_data.idCliente, cliente_data.nombreApellido)
        else:
            st.error("Cliente no encontrado.")

if __name__ == "__main__":
    main()