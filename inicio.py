import streamlit as st
from clientes_app import main as clientes_main
from pagos_app import main as pagos_main
from informacionClientes_app import main as info_clientes_main
from usuarios_app import main as usuarios_main
from modificaClientes_app import main as modifica_cliente_main
from modificaPagos_app import main as modifica_pagos_main
from gastos_app import main as gastos_main
from visualizarGastos_app import main as visualizar_gastos_main
import pyodbc
import json
import logging

# Configurar el registro
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Crear un objeto de registro para tu aplicación
logger = logging.getLogger(__name__)

# Crear una variable de sesión para almacenar el estado de inicio de sesión
logged_in = st.session_state.get("logged_in", False)

# Crear una variable de sesión para almacenar el nombre y apellido del usuario
user_nombre_apellido = st.session_state.get("user_nombre_apellido", "")

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Obtener una lista de nombres y apellidos de la base de datos
def obtener_nombres_apellidos():
    conn = pyodbc.connect(
        driver=config["driver"],
        server=config["server"],
        database=config["database"],
        uid=config["user"],
        pwd=config["password"]
    )
    cursor = conn.cursor()
    
    query = "SELECT CONCAT(nombre, ' ', apellido) FROM Usuario"
    cursor.execute(query)
    
    nombres_apellidos = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return nombres_apellidos

# Crear una función para verificar las credenciales y obtener el rol del usuario
def login(username, password):
    conn = pyodbc.connect(
        driver=config["driver"],
        server=config["server"],
        database=config["database"],
        uid=config["user"],
        pwd=config["password"]
    )
    cursor = conn.cursor()
    
    query = f"SELECT rol FROM Usuario WHERE CONCAT(nombre, ' ', apellido) = ? AND contraseña = ?"
    cursor.execute(query, (username, password))
    row = cursor.fetchone()
    
    if row:
        rol = row[0]
        st.session_state.logged_in = True
        st.session_state.rol = rol
        st.session_state.user_nombre_apellido = username  # Almacenar el nombre y apellido en la sesión
        st.success(f"Bienvenido, {username}! Inicio de sesión exitoso!")
        # Redirigir después de iniciar sesión
        st.experimental_rerun()  # Recargar la aplicación para mostrar el contenido correcto
    else:
        st.error("Credenciales incorrectas. Inténtalo de nuevo.")
    
    cursor.close()
    conn.close()

# Función para cerrar sesión
def logout():
    st.session_state.logged_in = False
    st.session_state.user_nombre_apellido = ""  # Limpiar el nombre y apellido al cerrar sesión
    st.success("Sesión cerrada exitosamente!")

def main():    
    st.title("SixGym - Sistema de Gestión")
    st.image("img\logo_SixGym.jpg", width=150)

    if logged_in:
        st.sidebar.title("Menú")
        
        if st.session_state.rol == "admin":
            selected_option = st.sidebar.selectbox("Seleccione una opción:", ["Inicio", "Ingresar Datos de Clientes", "Ingresar Pagos", "Información de Clientes", "Ingresar Usuarios", "Modificar Clientes", "Modificar Pagos", "Registrar Gastos", "Visualizar Gastos"])
            if selected_option == "Modificar Clientes":
                modifica_cliente_main()  # Carga la pestaña para modificar clientes en la misma página
            elif selected_option == "Modificar Pagos":
                modifica_pagos_main()  # Carga la pestaña para modificar pagos en la misma página
            elif selected_option == "Registrar Gastos":
                gastos_main()  # Agregar la pestaña para gestionar gastos en la misma página
            elif selected_option == "Visualizar Gastos":
                visualizar_gastos_main()  # Agregar la pestaña para gestionar gastos en la misma página
        else:
            selected_option = st.sidebar.selectbox("Seleccione una opción:", ["Inicio", "Ingresar Datos de Clientes", "Ingresar Pagos", "Información de Clientes"])
        
        if selected_option == "Inicio":
            st.write(f"Bienvenido, {user_nombre_apellido}! - SixGym - Sistema de Gestión")
        
        # Agregar una etiqueta que muestre el nombre del usuario
        st.write(f"Usuario: {user_nombre_apellido}")
        
        if selected_option == "Ingresar Datos de Clientes":
            clientes_main()
        elif selected_option == "Ingresar Pagos":
            pagos_main()
        elif selected_option == "Información de Clientes":
            info_clientes_main()
        elif selected_option == "Ingresar Usuarios":
            usuarios_main()
    else:
        st.sidebar.title("Inicio de Sesión")
        nombres_apellidos = obtener_nombres_apellidos()  # Obtener la lista de nombres y apellidos desde la base de datos
        username = st.selectbox("Nombre y Apellido:", nombres_apellidos)
        password = st.text_input("Contraseña:", type="password")
        if st.button("Iniciar Sesión"):
            login(username, password)
    
    # Mostrar opción de cerrar sesión si está autenticado
    if logged_in:
        st.sidebar.button("Cerrar Sesión", on_click=logout)

if __name__ == "__main__":
    main()
