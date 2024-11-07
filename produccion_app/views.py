
import datetime
import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import pandas as pd
from .utils import  filtrar_por_tiempo

@csrf_exempt
@require_http_methods(["POST"])
def InfoLote(request):
    
    data = json.loads(request.body)
    df = pd.DataFrame(data['produccion'])      
    tiempo = data.get('tiempo')
    
    # Filtramos el DataFrame por el tiempo deseado
    df_filtrado = filtrar_por_tiempo(df, tiempo)

    # Agrupar por fecha y sumar cantidades de producción
    df_agrupado = df_filtrado.groupby('fecha')['cantidad'].sum().reset_index()

    # Agrupar por vaca para producción total por vaca
    df_vaca = df_filtrado.groupby('vaca_id')['cantidad'].sum().reset_index()

    # Agrupar por lote para producción total por lote
    df_lote = df_filtrado.groupby('lote_id')['cantidad'].sum().reset_index()

    # Crear el diccionario estructurado para el JSON
    resultado = {
        "produccion_tiempo": df_agrupado.to_dict(orient="records"),
        "produccion_por_vaca": df_vaca.to_dict(orient="records"),
        "produccion_por_lote": df_lote.to_dict(orient="records")
    }
    return JsonResponse(resultado)

@csrf_exempt
@require_http_methods(["POST"])
def produccion_por_lote(request):
    
   # Cargar los datos recibidos en formato JSON
    data = json.loads(request.body)
    
    # Convertir los datos en un DataFrame de pandas
    df = pd.DataFrame(data['produccion'])  
    lote_id = data['lote_id']
    tiempo = data.get('tiempo', '1mes')  # Valor por defecto si 'tiempo' no se pasa
    
    # Filtrar datos por el periodo de tiempo y lote
    df_filtrado = filtrar_por_tiempo(df, tiempo)
    df_lote = df_filtrado[df_filtrado['lote_id'] == lote_id]

    # Agrupar por 'vaca_id' y sumar la cantidad de producción de cada vaca
    df_vaca_agrupado = df_lote.groupby('vaca_id')['cantidad'].sum().reset_index()

    # Agrupar por 'fecha' y sumar la cantidad de producción para el lote
    df_lote_agrupado = df_lote.groupby('fecha')['cantidad'].sum().reset_index()
    df_lote_agrupado['lote'] = f'Lote {lote_id}'

    # Convertir 'fecha' a formato de texto (str) para evitar problemas con JSON
    df_lote_agrupado['fecha'] = df_lote_agrupado['fecha'].astype(str)
    df_lote_agrupado['cantidad'] = df_lote_agrupado['cantidad'].astype(float)  # Asegurarse de que 'cantidad' sea float

    # Asegurarse de que los datos son serializables
    df_vaca_agrupado['cantidad'] = df_vaca_agrupado['cantidad'].astype(float)
    df_vaca_agrupado['vaca_id'] = df_vaca_agrupado['vaca_id'].astype(int)

    # Convertir el DataFrame a un formato que pueda ser serializado como JSON
    resultado = {
        "produccion_por_vaca": df_vaca_agrupado.to_dict(orient="records"),
        "produccion_por_lote": df_lote_agrupado.to_dict(orient="records")
    }
    

    return JsonResponse(resultado)

@csrf_exempt
@require_http_methods(["POST"])
def comparar_lotes(request):
    data = json.loads(request.body)
    df = pd.DataFrame(data['produccion'])  
    lote_id1 = data['lote_id1']
    lote_id2 = data['lote_id2']
    tiempo = data.get('tiempo')
    
    # Filtrar datos por tiempo
    df_filtrado = filtrar_por_tiempo(df, tiempo)
    
    # Filtrar por cada lote
    df_lote1 = df_filtrado[df_filtrado['lote_id'] == lote_id1]
    df_lote2 = df_filtrado[df_filtrado['lote_id'] == lote_id2]

    # Agrupar por fecha y sumar las cantidades de producción para cada lote
    df_lote1_agrupado = df_lote1.groupby('fecha')['cantidad'].sum().reset_index()
    df_lote2_agrupado = df_lote2.groupby('fecha')['cantidad'].sum().reset_index()
    
    df_lote1_agrupado['fecha'] = df_lote1_agrupado['fecha'].astype(str)
    df_lote1_agrupado['cantidad'] = df_lote1_agrupado['cantidad'].astype(float)
    df_lote2_agrupado['fecha'] = df_lote2_agrupado['fecha'].astype(str)
    df_lote2_agrupado['cantidad'] = df_lote2_agrupado['cantidad'].astype(float)

    # Agregar una columna para identificar el lote en los datos
    df_lote1_agrupado['lote'] = f'Lote {lote_id1}'
    df_lote2_agrupado['lote'] = f'Lote {lote_id2}'

    # Combinar ambos DataFrames para la comparación
    df_combinado = pd.concat([df_lote1_agrupado, df_lote2_agrupado])

    # Calcular la producción total de cada lote
    total_lote1 = float(df_lote1['cantidad'].sum())
    total_lote2 = float(df_lote2['cantidad'].sum())

    # Crear el resultado estructurado en un diccionario
    resultado = {
        "comparacion_por_fecha": df_combinado.to_dict(orient="records"),
        "produccion_total": {
            f"Lote {lote_id1}": total_lote1,
            f"Lote {lote_id2}": total_lote2
        }
    }

    return JsonResponse(resultado)
@csrf_exempt
@require_http_methods(["POST"])
def procesar_comparacion_vacas(request):
  
    data = json.loads(request.body)
    df = pd.DataFrame(data['produccion'])  
    vaca_id1 = data['vaca_id1']
    vaca_id2 = data['vaca_id2']
    tiempo = data.get('tiempo')

      # Filtrar datos por tiempo
    df_filtrado = filtrar_por_tiempo(df, tiempo)
    df_vaca1 = df_filtrado[df_filtrado['vaca_id'] == vaca_id1]
    df_vaca2 = df_filtrado[df_filtrado['vaca_id'] == vaca_id2]

    # Agrupar por fecha y sumar cantidades de producción para cada vaca
    df_vaca1_agrupado = df_vaca1.groupby('fecha')['cantidad'].sum().reset_index()
    df_vaca2_agrupado = df_vaca2.groupby('fecha')['cantidad'].sum().reset_index()

    # Convertir las columnas 'fecha' y 'cantidad' a tipos estándar de Python
    df_vaca1_agrupado['fecha'] = df_vaca1_agrupado['fecha'].astype(str)
    df_vaca1_agrupado['cantidad'] = df_vaca1_agrupado['cantidad'].astype(float)
    df_vaca2_agrupado['fecha'] = df_vaca2_agrupado['fecha'].astype(str)
    df_vaca2_agrupado['cantidad'] = df_vaca2_agrupado['cantidad'].astype(float)

    # Agregar una columna para identificar la vaca en los datos
    df_vaca1_agrupado['vaca'] = f'Vaca {vaca_id1}'
    df_vaca2_agrupado['vaca'] = f'Vaca {vaca_id2}'

    # Combinar ambos DataFrames para la comparación
    df_combinado = pd.concat([df_vaca1_agrupado, df_vaca2_agrupado])

    # Calcular la producción total de cada vaca
    total_vaca1 = float(df_vaca1['cantidad'].sum())
    total_vaca2 = float(df_vaca2['cantidad'].sum())

    # Crear el resultado estructurado en un diccionario
    resultado = {
        "comparacion_por_fecha": df_combinado.to_dict(orient="records"),
        "produccion_total": {
            f"Vaca {vaca_id1}": total_vaca1,
            f"Vaca {vaca_id2}": total_vaca2
        }
    }

    # Enviar la respuesta como JSON
    return JsonResponse(resultado)

