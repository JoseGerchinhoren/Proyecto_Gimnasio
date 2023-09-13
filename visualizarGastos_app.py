import streamlit as st
import pyodbc
import pandas as pd
import json
import base64

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

def visualizar_gastos():
    st.title("Visualizar Gastos")

    # Consulta SQL para obtener los gastos
    query = """
    SELECT idGasto, fecha, motivo, lugar, monto, metodoPago, categoria, observacion, rutaArchivo, archivo
    FROM Gasto
    ORDER BY idGasto DESC
    """

    # Ejecutar la consulta y obtener los resultados en un DataFrame
    gastos_df = pd.read_sql(query, db)

    # Mostrar la tabla de gastos
    st.dataframe(gastos_df)

    # Agregar enlaces para descargar archivos
    for index, row in gastos_df.iterrows():
        archivo_data = row['archivo']
        if archivo_data:
            b64 = base64.b64encode(archivo_data).decode('utf-8')
            st.markdown(f"**Descargar Archivo #{index + 1}**")
            st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="archivo_{index + 1}.pdf">Descargar PDF</a>', unsafe_allow_html=True)

def main():
    visualizar_gastos()

if __name__ == "__main__":
    main()