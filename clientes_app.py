import streamlit as st

def main():
    st.title("Ingresar Datos de Clientes")
    
    nombre = st.text_input("Nombre del Cliente:")
    edad = st.number_input("Edad:", min_value=0, max_value=120, value=25)
    email = st.text_input("Email:")
    
    if st.button("Guardar Cliente"):
        st.success(f"Cliente {nombre} guardado exitosamente!")

if __name__ == "__main__":
    main()
