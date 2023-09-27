from datetime import datetime

def calcular_estado_cuota(ultima_fecha_pago, fecha_actual, fecha_vencimiento):
    if ultima_fecha_pago:
        diferencia_dias = fecha_actual - ultima_fecha_pago
        diferencia_dias_vencimiento = fecha_vencimiento - fecha_actual

        if diferencia_dias.days > 0:
            estado_texto = "Cuota vencida"
            estado_color = "red"
        elif diferencia_dias_vencimiento.days <= 0:
            estado_texto = "Cuota al día"
            estado_color = "green"
        else:
            estado_texto = "Cuota próxima a vencer"
            estado_color = "orange"
    else:
        estado_texto = "Sin pagos registrados"
        estado_color = "gray"

    return estado_texto, estado_color

# Obtener la fecha actual
fecha_actual = datetime.now()

# Obtener la fecha del último pago
fecha_ultimo_pago = datetime(2023, 8, 28)

# Llamar a la función
estado_texto, estado_color = calcular_estado_cuota(fecha_ultimo_pago, fecha_actual)

# Imprimir los resultados
print(f"Estado: {estado_texto}")
print(f"Color: {estado_color}")