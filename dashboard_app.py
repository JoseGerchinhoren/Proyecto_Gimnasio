import streamlit as st
import pandas as pd
import mysql.connector
import json

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Conexión a la base de datos MySQL
db = mysql.connector.connect(
    host=config["host"],
    user=config["user"],
    password=config["password"],
    database=config["database"]
)

def obtener_datos_dashboard():
    cursor = db.cursor()
    query = "SELECT fechaPago, montoPago FROM Pagos"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

def obtener_cantidad_socios_actuales():
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM Clientes"
    cursor.execute(query)
    cantidad_socios = cursor.fetchone()[0]
    cursor.close()
    return cantidad_socios

def main():
    st.title("SixGym - Dashboard")
    
    data = obtener_datos_dashboard()
    df = pd.DataFrame(data, columns=["Mes", "Ingresos"])
    
    st.write("Ingresos por Mes")
    st.line_chart(df.set_index("Mes"))
    
    objetivo_ingreso_mensual = 10000
    cantidad_socios = obtener_cantidad_socios_actuales()
    
    st.write("KPIs")
    
    # Indicadores de estado
    if df['Ingresos'].sum() >= objetivo_ingreso_mensual:
        st.success("Objetivo de Ingreso Mensual Cumplido")
    else:
        st.error("Objetivo de Ingreso Mensual Pendiente")
    
    if cantidad_socios > 2:
        st.success("Socios Suficientes")
    else:
        st.warning("Socios Insuficientes")
    
    # Valores numéricos
    st.write(f"Ingresos Totales: ${df['Ingresos'].sum()}")
    st.write(f"Ingreso Promedio por Mes: ${df['Ingresos'].mean():.2f}")
    st.write(f"Objetivo de Ingreso por Mes: ${objetivo_ingreso_mensual}")
    st.write(f"Cantidad de Socios Actuales: {cantidad_socios}")

if __name__ == "__main__":
    main()
