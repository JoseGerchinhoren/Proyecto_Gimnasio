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

def guardar_gasto(fecha, motivo, lugar, monto, metodo_pago, categoria_gasto, observacion, ruta_archivo, archivo):
    cursor = db.cursor()
    query = """
        INSERT INTO Gasto (fecha, motivo, lugar, monto, metodoPago, categoria, observacion, rutaArchivo, archivo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    values = (fecha, motivo, lugar, monto, metodo_pago, categoria_gasto, observacion, ruta_archivo, archivo)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

def main():
    st.title("Ingresar Gastos")
    
    fecha = st.date_input("Fecha:", key="fecha")
    motivo = st.text_input("Motivo del Gasto:", key="motivo")
    lugar = st.text_input("Lugar del Gasto:", key="lugar")
    monto = st.number_input("Monto del Gasto:", min_value=0, format="%d", key="monto")
    
    # Campo de método de pago como un desplegable
    metodo_pago_options = ["Efectivo", "Transferencia", "Tarjeta", "Otro"]
    metodo_pago = st.selectbox("Método de Pago:", metodo_pago_options, key="metodo_pago")
    
    # Campo de categoría de gasto como un desplegable
    categoria_gasto_options = ["Mantenimiento", "Suministros", "Alquiler", "Insumos", "Pago Empleados", "Otro"]
    categoria_gasto = st.selectbox("Categoría del Gasto:", categoria_gasto_options, key="categoria_gasto")
    
    observacion = st.text_area("Observación:", key="observacion")
    
    ruta_archivo = st.text_input("Ruta de Archivo:", key="ruta_archivo")
    
    archivo = st.file_uploader("Subir Archivo (PDF o Imagen):", type=["pdf", "jpg", "jpeg", "png"])
    
    if st.button("Guardar Gasto"):
        if motivo and lugar and monto and metodo_pago and categoria_gasto and observacion:
            # Verificar si se cargó un archivo
            archivo_data = None
            if archivo:
                archivo_data = archivo.read()
            
            guardar_gasto(fecha, motivo, lugar, monto, metodo_pago, categoria_gasto, observacion, ruta_archivo, archivo_data)
            st.success("Gasto guardado exitosamente!")
        else:
            st.warning("Complete todos los campos obligatorios antes de guardar el gasto.")

if __name__ == "__main__":
    main()
