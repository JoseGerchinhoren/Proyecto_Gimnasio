from datetime import datetime
from dateutil import relativedelta

def calcular_estado_cuota(ultima_fecha_pago, fecha_actual):
    if ultima_fecha_pago:
        # Obtener la fecha de hoy como datetime.date si es un objeto datetime.datetime
        if isinstance(fecha_actual, datetime):
            fecha_actual = fecha_actual.date()

        # Calcular la fecha de vencimiento (1 mes después de la última fecha de pago)
        fecha_vencimiento = ultima_fecha_pago + relativedelta.relativedelta(months=1)

        if fecha_actual < fecha_vencimiento:
            estado_texto = "Cuota al día"
            estado_color = "green"
        elif fecha_actual == fecha_vencimiento:
            estado_texto = "Vence hoy"
            estado_color = "yellow"
        else:
            estado_texto = "Cuota vencida"
            estado_color = "red"
    else:
        estado_texto = "Sin pagos registrados"
        estado_color = "gray"

    return estado_texto, estado_color

# Obtener la fecha actual
fecha_actual = datetime.today()  # Fecha de ejemplo

# Obtener la fecha del último pago
fecha_ultimo_pago = datetime(2023, 8, 28)  # Fecha de ejemplo

# Llamar a la función
estado_texto, estado_color = calcular_estado_cuota(fecha_ultimo_pago, fecha_actual)

# Imprimir los resultados
print(f"Estado: {estado_texto}")
print(f"Color: {estado_color}")
print(fecha_actual)
