from django.urls import path
from . import views

urlpatterns = [
    path('info-lotes/', views.InfoLote, name='procesar_info_lotes'),
    path('produccion-lote/', views.produccion_por_lote, name='produccion_lote'),
    path('comparar-lotes/', views.comparar_lotes, name='comparar_lotes'),
    path('comparar-vacas/', views.procesar_comparacion_vacas, name='comparar_vacas'),
]