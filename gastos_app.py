import streamlit as st

def main():
    st.title("Registrar Gastos")
    
    fecha = st.date_input("Fecha:")
    motivo = st.text_input("Motivo del Gasto:")
    lugar = st.text_input("Lugar del Gasto:")
    monto = st.number_input("Monto:", min_value=0)
    metodo_pago = st.selectbox("Método de Pago:", ["Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito", "Transferencia", "Otro"])
    categoria_gasto = st.selectbox("Categoría del Gasto:", ["Mantenimiento", "Suministros", "Alquiler", "Insumos", "Pago Empleados","Otro"])
    observacion = st.text_area("Observación:")

    if st.button("Registrar Gasto"):
        st.success(f"Gasto registrado:\n"
                   f"Monto: ${monto}\n"
                   f"Fecha: {fecha}\n"
                   f"Motivo: {motivo}\n"
                   f"Lugar: {lugar}\n"
                   f"Método de Pago: {metodo_pago}\n"
                   f"Categoría del Gasto: {categoria_gasto}\n"
                   f"Observación: {observacion}")

if __name__ == "__main__":
    main()
