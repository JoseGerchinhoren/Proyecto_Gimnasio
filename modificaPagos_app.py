import streamlit as st
import pyodbc
import json
import pandas as pd

# Cargar configuración desde el archivo config.json
with open("../config.json") as config_file:
    config = json.load(config_file)

# Función para conectar a la base de datos
def conectar_bd():
    return pyodbc.connect(
        driver=config["driver"],
        server=config["server"],
        database=config["database"],
        uid=config["user"],
        pwd=config["password"]
    )

# Función para obtener los nombres de los clientes
def obtener_nombres_clientes():
    conn = conectar_bd()
    cursor = conn.cursor()
    
    query = "SELECT C.nombreApellido FROM Cliente AS C INNER JOIN Pago AS P ON C.idCliente = P.idCliente GROUP BY C.nombreApellido"
    cursor.execute(query)
    nombres_clientes = [cliente[0] for cliente in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return nombres_clientes

# Función para obtener los pagos de un cliente por su nombre y apellido
def obtener_pagos_cliente(nombre_apellido):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    query = """
    SELECT P.idCliente, P.idPago, P.fechaPago, P.montoPago, P.metodoPago, P.detallePago
    FROM Pago AS P
    INNER JOIN Cliente AS C ON P.idCliente = C.idCliente
    WHERE C.nombreApellido = ?
    ORDER BY idPago DESC
    """
    
    cursor.execute(query, (nombre_apellido,))
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return rows  # Devuelve una lista de filas de datos de pagos del cliente

# Función para obtener el ID de usuario a partir de su nombre y apellido
def obtener_id_usuario(nombre, apellido):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    query = """
    SELECT idUsuario
    FROM Usuario
    WHERE nombre = ? AND apellido = ?
    """
    
    cursor.execute(query, (nombre, apellido))
    row = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    return row[0] if row else None  # Devuelve el ID de usuario o None si no se encuentra

# Función para editar un pago por su ID
def editar_pago(id_pago, monto, metodo_pago, detalle_pago, nombre_usuario, campo_editado, nuevo_valor):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    # Obtener el valor anterior del campo editado
    query_valor_anterior = f"""
    SELECT {campo_editado}
    FROM Pago
    WHERE idPago = ?
    """
    cursor.execute(query_valor_anterior, (id_pago,))
    valor_anterior = cursor.fetchone()[0]

    # Realizar la actualización en la tabla Pago
    query = """
    UPDATE Pago
    SET
        montoPago = ?,
        metodoPago = ?,
        detallePago = ?
    WHERE idPago = ?
    """
    values = (monto, metodo_pago, detalle_pago, id_pago)
    cursor.execute(query, values)
    
    # Obtener el ID de usuario a partir del nombre y apellido del usuario
    nombre, apellido = nombre_usuario.split(" ")  # Divide el nombre y el apellido
    id_usuario_modificacion = obtener_id_usuario(nombre, apellido)
   
    # Registrar la modificación en la tabla ModificacionesPagos
    query_modificacion = """
    INSERT INTO ModificacionesPagos (idPago, idUsuario, fechaModificacion, campoModificado, valorAnterior)
    VALUES (?, ?, GETDATE(), ?, ?)
    """
    values_modificacion = (id_pago, id_usuario_modificacion, campo_editado, valor_anterior)
    cursor.execute(query_modificacion, values_modificacion)
    
    conn.commit()
    cursor.close()
    conn.close()

def eliminar_pago(id_pago, nombre_cliente):
    conn = conectar_bd()
    cursor = conn.cursor()

    try:
        # Obtener los detalles del pago que se va a eliminar
        query_obtener_pago = """
        SELECT idCliente, fechaPago, horarioPago, montoPago, metodoPago, detallePago, idUsuario
        FROM Pago
        WHERE idPago = ?
        """
        cursor.execute(query_obtener_pago, (id_pago,))
        detalle_pago = cursor.fetchone()
        if detalle_pago:
            id_cliente, fecha_pago, horario_pago, monto_pago, metodo_pago, detalle_pago, id_usuario_creacion = detalle_pago
            
            # Insertar los detalles del pago eliminado en la tabla pagosEliminados
            query_insertar_pago_eliminado = """
            INSERT INTO PagosEliminados (idPago, idCliente, idUsuario, fechaEliminacion, fechaPago, horarioPago, montoPago, metodoPago, detallePago)
            VALUES (?, ?, ?, GETDATE(), ?, ?, ?, ?, ?)
            """
            
            cursor.execute(query_insertar_pago_eliminado, (id_pago, id_cliente, id_usuario_creacion, fecha_pago, horario_pago, monto_pago, metodo_pago, detalle_pago))
            
            # Eliminar el pago de la tabla Pago
            query_eliminar_pago = """
            DELETE FROM Pago WHERE idPago = ?
            """
            cursor.execute(query_eliminar_pago, (id_pago,))
            conn.commit()
            st.success(f"Se ha eliminado el pago con ID {id_pago} correctamente y se ha registrado en la tabla de pagos eliminados.")
        else:
            st.warning(f"No se encontró el pago con ID {id_pago}.")
    except pyodbc.IntegrityError as e:
        st.error(f"No se puede eliminar el pago con ID {id_pago} debido a restricciones de integridad en la base de datos. Asegúrese de que no existan registros relacionados en otras tablas.")
    except Exception as e:
        st.error(f"Se produjo un error al eliminar el pago con ID {id_pago}: {str(e)}")
    finally:
        cursor.close()
        conn.close()

def buscar_pagos_por_fecha(fecha_pago):
    conn = conectar_bd()
    cursor = conn.cursor()
    
    query = """
    SELECT P.idCliente, P.idPago, P.fechaPago, P.montoPago, P.metodoPago, P.detallePago
    FROM Pago AS P
    INNER JOIN Cliente AS C ON P.idCliente = C.idCliente
    WHERE P.fechaPago = ?
    ORDER BY idPago DESC
    """
    
    cursor.execute(query, (fecha_pago,))
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return rows

def main():
    st.title("Modificar Pagos de Clientes")
    
    # Obtener nombre y apellido del usuario autenticado
    user_nombre_apellido = st.session_state.user_nombre_apellido
    
    # Obtener la lista de nombres y apellidos de los clientes desde la base de datos
    nombres_clientes = obtener_nombres_clientes()

    st.title("Buscar Cliente")

    nombres_clientes = obtener_nombres_clientes()
    nombre_cliente_input = st.text_input("Ingrese el Nombre y Apellido del Cliente:")
    selected_cliente = None
    
    if nombre_cliente_input:
        nombres_coincidentes = [nombre for nombre in nombres_clientes if nombre_cliente_input.lower() in nombre.lower()]
        if nombres_coincidentes:
            selected_cliente = st.selectbox("Seleccione un nombre:", nombres_coincidentes)
    
    if selected_cliente:
        st.title(f"Cliente seleccionado: {selected_cliente}")
        # Obtener los pagos del cliente
        pagos_cliente = obtener_pagos_cliente(selected_cliente)
        
        if pagos_cliente:
            st.write(f"Pagos de {selected_cliente}, ordenados del más nuevo al más antiguo:")

            # Crear una lista de tuplas a partir de los datos de pagos_cliente
            pagos_data = [(p[0], p[1], p[2], p[3], p[4], p[5]) for p in pagos_cliente]
            # Crear el DataFrame con las columnas especificadas
            pagos_df = pd.DataFrame(pagos_data, columns=["idCliente", "idPago", "fechaPago", "montoPago", "metodoPago", "detallePago"])
            st.dataframe(pagos_df)
            
            # Permitir al usuario seleccionar un pago para editar por su ID
            id_pago = st.number_input("ID del Pago a Editar", min_value=1)

            if id_pago:
                # Verificar si el ID del pago ingresado pertenece al cliente
                if any(pago[1] == id_pago for pago in pagos_cliente):
                    st.write("Información del Pago:")
                    
                    # Encontrar el pago seleccionado
                    pago_seleccionado = next(pago for pago in pagos_cliente if pago[1] == id_pago)
                    idCliente, id_pago, fecha_pago, monto_pago, metodo_pago, detalle_pago = pago_seleccionado
                    
                    # Mostrar toda la información del pago
                    st.write(f"ID de Pago: {id_pago}")
                    st.write(f"Fecha de Pago: {fecha_pago}")
                    st.write(f"Monto: {monto_pago}")
                    st.write(f"Método de Pago: {metodo_pago}")
                    st.write(f"Detalle de Pago: {detalle_pago}")
                    
                    st.write("Editar Campos:")
                    
                    # Permitir al usuario seleccionar el campo del pago que desea editar
                    campos_editables = ["Monto", "Método de Pago", "Detalle de Pago"]
                    campo_editar = st.selectbox("Seleccione el campo a editar:", campos_editables)
                    
                    # Habilitar la edición solo para los campos seleccionados
                    if campo_editar == "Monto":
                        nuevo_valor = float(st.number_input("Nuevo Monto", value=float(monto_pago)))
                    elif campo_editar == "Método de Pago":
                        nuevo_valor = st.text_input("Nuevo Método de Pago", value=metodo_pago)
                    elif campo_editar == "Detalle de Pago":
                        nuevo_valor = st.text_area("Nuevo Detalle de Pago", value=detalle_pago)
                    else:
                        nuevo_valor = None
                    
                    if st.button("Guardar Cambios") and nuevo_valor is not None:
                        # Realizar la edición del campo seleccionado
                        if campo_editar == "Monto":
                            editar_pago(id_pago, nuevo_valor, metodo_pago, detalle_pago, user_nombre_apellido, "montoPago", nuevo_valor)
                        elif campo_editar == "Método de Pago":
                            editar_pago(id_pago, monto_pago, nuevo_valor, detalle_pago, user_nombre_apellido, "metodoPago", nuevo_valor)
                        elif campo_editar == "Detalle de Pago":
                            editar_pago(id_pago, monto_pago, metodo_pago, nuevo_valor, user_nombre_apellido, "detallePago", nuevo_valor)
                        
                        st.success(f"Se ha editado el campo {campo_editar} correctamente.")
                    # Agregar un botón para eliminar el pago
                    if st.button("Eliminar Pago"):
                        eliminar_pago(id_pago, selected_cliente)
                else:
                    st.error("ID de Pago no válido para este cliente.")
            else:
                st.warning("Ingrese un ID de Pago válido para editar.")

        else:
            st.warning(f"No se encontraron pagos para {selected_cliente}.")

if __name__ == "__main__":
    main()
