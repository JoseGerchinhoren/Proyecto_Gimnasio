import streamlit as st
from clientes_app import main as clientes_main
from pagos_app import main as pagos_main
from informacionClientes_app import main as info_clientes_main

def main():
    st.title("SixGym - Sistema de Gestión")
    
    st.sidebar.title("Menú")
    selected_option = st.sidebar.selectbox("Seleccione una opción:", ["Inicio", "Ingresar Datos de Clientes", "Ingresar Pagos", "Información de Clientes"])
    
    if selected_option == "Inicio":
        st.write("Bienvenido a SixGym - Sistema de Gestión")
    elif selected_option == "Ingresar Datos de Clientes":
        clientes_main()
    elif selected_option == "Ingresar Pagos":
        pagos_main()
    elif selected_option == "Información de Clientes":
        info_clientes_main()

if __name__ == "__main__":
    main()
