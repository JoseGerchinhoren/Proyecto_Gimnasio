import streamlit as st
import pyodbc
import json
from datetime import datetime

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Conexión a la base de datos SQL Server
conn = pyodbc.connect(
    driver=config["driver"],
    server=config["server"],
    database=config["database"],
    uid=config["user"],
    pwd=config["password"]
)

# Función para validar el formato de fecha DD/MM/AAAA
def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, '%d/%m/%Y')
        return True
    except ValueError:
        return False

# Función para obtener el ID de usuario a partir de su nombre y apellido
def obtener_id_usuario(nombre, apellido):
    cursor = conn.cursor()
    
    query = """
    SELECT idUsuario
    FROM Usuario
    WHERE nombre = ? AND apellido = ?
    """
    
    cursor.execute(query, (nombre, apellido))
    row = cursor.fetchone()
    
    cursor.close()
    
    return row[0] if row else None  # Devuelve el ID de usuario o None si no se encuentra

# Modificar la función guardar_cliente
def guardar_cliente(fecha_inscripcion, fecha_nacimiento, nombre_apellido, genero, email, telefono, domicilio, dni, motivo_gym, como_se_entero, observaciones, idUsuario):
    cursor = conn.cursor()
    
    # Obtener el ID de usuario a partir del nombre y apellido del usuario
    nombre, apellido = idUsuario.split(" ")  # Divide el nombre y el apellido
    id_usuario = obtener_id_usuario(nombre, apellido)

    try:
        # Validar el formato de la fecha de nacimiento
        if not validar_fecha(fecha_nacimiento):
            st.error("Error: La fecha de nacimiento no se ingresó en el formato correcto (DD/MM/AAAA).")
            return
        
        # Convertir la fecha de nacimiento al formato 'AAAA-MM-DD'
        fecha_nacimiento_sql = datetime.strptime(fecha_nacimiento, '%d/%m/%Y').strftime('%Y-%m-%d')

        # Ejecutar el stored procedure con los parámetros requeridos
        cursor.execute("EXEC InsertarCliente ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
                    (fecha_inscripcion, fecha_nacimiento_sql, nombre_apellido, genero, email, telefono, domicilio, dni, motivo_gym, como_se_entero, observaciones, id_usuario))
        conn.commit()
        st.success(f"Cliente {nombre_apellido} guardado exitosamente!")

    except pyodbc.Error as e:
        conn.rollback()
        st.error(f"Error al guardar el Cliente: {str(e)}")
    finally:
        cursor.close()

def main():
    st.title("Ingresar Datos de Clientes")
    
    fecha_inscripcion = st.date_input("Fecha de Inscripción:") 
    nombre_apellido = st.text_input("Nombre/s y Apellido/s del Cliente:")
    fecha_nacimiento = st.text_input("Fecha de Nacimiento (DD/MM/AAAA):")
    genero_options = ["Masculino", "Femenino", "Otro"]
    genero = st.selectbox("Género:", genero_options)
    email = st.text_input("Email:")
    telefono = st.text_input("Número de Teléfono Celular:")
    domicilio = st.text_input("Domicilio:")
    dni = st.text_input("Número de DNI:")
    motivo_gym = st.text_input("Motivo por el cual viene al gym:")
    como_se_entero = st.text_input("¿Cómo se enteró de Six Gym?")
    observaciones = st.text_area("Observaciones")
    
    # Obtener el nombre y apellido del usuario autenticado
    idUsuario = st.session_state.get("user_nombre_apellido", "")
    
    if st.button("Guardar Cliente"):
        try:
            guardar_cliente(fecha_inscripcion, fecha_nacimiento, nombre_apellido, genero, email, telefono, domicilio, dni, motivo_gym, como_se_entero, observaciones, idUsuario)
        except Exception as e:
            st.error(f"Error al guardar el cliente: {str(e)}")
        
if __name__ == "__main__":
    main()
