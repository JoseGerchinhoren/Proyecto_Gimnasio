import streamlit as st

def main():
    st.title("Registrar Gastos")
    
    descripcion = st.text_input("Descripción del Gasto:")
    monto = st.number_input("Monto:", min_value=0)
    fecha = st.date_input("Fecha:")
    
    if st.button("Registrar Gasto"):
        st.success(f"Gasto de {descripcion} por ${monto} registrado el {fecha}")

if __name__ == "__main__":
    main()
