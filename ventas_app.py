import streamlit as st

def main():
    st.title("Registrar Ventas")
    
    producto = st.text_input("Producto:")
    monto = st.number_input("Monto:", min_value=0)
    fecha = st.date_input("Fecha:")
    
    if st.button("Registrar Venta"):
        st.success(f"Venta de {producto} por ${monto} registrada el {fecha}")

if __name__ == "__main__":
    main()
