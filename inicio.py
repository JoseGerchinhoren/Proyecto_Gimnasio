import streamlit as st
from clientes_app import main as clientes_main
from pagos_app import main as pagos_main
from informacionClientes_app import main as info_clientes_main
from usuarios_app import main as usuarios_main

# Crear una variable de sesión para almacenar el estado de inicio de sesión
logged_in = st.session_state.get("logged_in", False)

# Función para verificar las credenciales de inicio de sesión
def login():
    username = st.text_input("Nombre de Usuario:")
    password = st.text_input("Contraseña:", type="password")
    if username == "admin" and password == "contraseña_admin":  # Aquí debes implementar la lógica de autenticación real
        st.session_state.logged_in = True
        st.success("Inicio de sesión exitoso!")
    else:
        st.error("Credenciales incorrectas. Inténtalo de nuevo.")

# Función para cerrar sesión
def logout():
    st.session_state.logged_in = False
    st.success("Sesión cerrada exitosamente!")

def main():
    st.title("SixGym - Sistema de Gestión")
    
    if logged_in:
        st.sidebar.title("Menú")
        selected_option = st.sidebar.selectbox("Seleccione una opción:", ["Inicio", "Ingresar Datos de Clientes", "Ingresar Pagos", "Información de Clientes", "Ingresar Usuarios"])
        
        if selected_option == "Inicio":
            st.write("Bienvenido a SixGym - Sistema de Gestión")
        elif selected_option == "Ingresar Datos de Clientes":
            clientes_main()
        elif selected_option == "Ingresar Pagos":
            pagos_main()
        elif selected_option == "Información de Clientes":
            info_clientes_main()
        elif selected_option == "Ingresar Usuarios":
            usuarios_main()
    else:
        st.sidebar.title("Inicio de Sesión")
        login()
    
    # Mostrar opción de cerrar sesión si está autenticado
    if logged_in:
        st.sidebar.button("Cerrar Sesión", on_click=logout)

if __name__ == "__main__":
    main()
