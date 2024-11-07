import datetime
import pandas as pd
def filtrar_por_tiempo(df, tiempo):
    today = datetime.datetime.now()  # Fecha actual
    if tiempo == '7dias':
        start_date = today - datetime.timedelta(days=7)
    elif tiempo == '1mes':
        start_date = today - datetime.timedelta(days=30)
    elif tiempo == '1año':
        start_date = today - datetime.timedelta(days=365)
    elif tiempo == '5años':
        start_date = today - datetime.timedelta(days=5 * 365)

    # Convertir la columna 'fecha' a datetime si no lo es
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  # 'errors=coerce' convertirá errores a NaT (Not a Time)

    # Filtrar los registros basados en la fecha
    return df[df['fecha'] >= start_date]

