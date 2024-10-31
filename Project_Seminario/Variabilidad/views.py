import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from django.shortcuts import render
from django.conf import settings
from io import BytesIO
import base64

def analisis_ventas(request):
    # Cargar archivo Excel
    filepath = os.path.join(settings.BASE_DIR, 'ventas_agosto-septiembre_2024.xlsx')
    ventas = pd.read_excel(filepath)

    # Convertir 'Fecha de Venta' a datetime
    ventas['Fecha de Venta'] = pd.to_datetime(ventas['Fecha de Venta'])

    # Obtener y traducir los nombres de los días
    english = ventas['Fecha de Venta'].dt.day_name()
    day_name_mapping = {
        'Monday': 'Lunes', 'Tuesday': 'Martes', 'Wednesday': 'Miércoles',
        'Thursday': 'Jueves', 'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
    }
    spanish = english.map(day_name_mapping)

    # Análisis de ventas diarias por día de la semana
    ventas_por_dia = ventas.groupby(spanish)['Cantidad Vendida'].sum()
    dias_semana_ordenados = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    ventas_por_dia = ventas_por_dia.reindex(dias_semana_ordenados)

    # Gráfico de ventas por día de la semana
    fig1 = plt.figure(figsize=(10, 6))
    sns.barplot(x=ventas_por_dia.index, y=ventas_por_dia.values)
    plt.title('Ventas por Día de la Semana')
    plt.xlabel('Día de la Semana')
    plt.ylabel('Cantidad Vendida')
    plt.xticks(rotation=45)
    img1 = BytesIO()
    fig1.savefig(img1, format='png')
    img1.seek(0)
    chart1_url = base64.b64encode(img1.getvalue()).decode()

    # Evolución mensual de las ventas
    ventas['Mes'] = ventas['Fecha de Venta'].dt.month
    ventas_mensuales = ventas.groupby('Mes')['Cantidad Vendida'].sum()

    fig2 = plt.figure(figsize=(10, 6))
    ventas_mensuales.plot(kind='line', marker='o')
    plt.title('Tendencia de Ventas Mensuales')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad Vendida')
    plt.grid(True)
    img2 = BytesIO()
    fig2.savefig(img2, format='png')
    img2.seek(0)
    chart2_url = base64.b64encode(img2.getvalue()).decode()

    # Descomposición de series temporales
    ventas_diarias = ventas.resample('D', on='Fecha de Venta')['Cantidad Vendida'].sum()
    resultado_descomposicion = seasonal_decompose(ventas_diarias, model='additive', period=7)

    fig3 = resultado_descomposicion.plot()
    img3 = BytesIO()
    fig3.savefig(img3, format='png')
    img3.seek(0)
    chart3_url = base64.b64encode(img3.getvalue()).decode()

    # Calcular métricas de variabilidad
    variabilidad_diaria = ventas_por_dia.std()
    variabilidad_mensual = ventas_mensuales.std()

    # Contexto para la plantilla
    context = {
        'chart1': chart1_url,
        'chart2': chart2_url,
        'chart3': chart3_url,
        'variabilidad_diaria': variabilidad_diaria,
        'variabilidad_mensual': variabilidad_mensual,
    }
    return render(request, 'Variabilidad.html', context)

