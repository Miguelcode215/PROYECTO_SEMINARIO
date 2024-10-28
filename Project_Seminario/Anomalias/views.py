import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usar el backend Agg
import matplotlib.pyplot as plt 
from sklearn.ensemble import IsolationForest
import numpy as np
import os
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render

def Deteccion_Anomalias(request):
    # Carga el archivo Excel
    filepath = os.path.join(settings.BASE_DIR, 'ventas_agosto-septiembre_2024.xlsx')
    df = pd.read_excel(filepath)
    print("ya cargó la data:")
    
    # Procesamiento de datos
    df['Fecha de Venta'] = pd.to_datetime(df['Fecha de Venta'])
    daily_sales = df.groupby(['Fecha de Venta', 'Producto'])['Cantidad Vendida'].sum().unstack().fillna(0)

    # Visualización de ventas diarias de productos seleccionados
    sample_products = daily_sales.columns[:4]
    plt.figure(figsize=(12, 6))
    daily_sales[sample_products].plot()
    plt.title("Ventas Diarias de Productos Seleccionados")
    plt.ylabel("Cantidad Vendida")
    plt.xlabel("Fecha")
    plt.legend(title="Productos")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Guardar la gráfica en un directorio
    save_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'grafica.png')
    plt.savefig(save_path, format='png')
    plt.close()  # Cierra la figura después de guardarla

    # Detección de anomalías
    isolation_forest = IsolationForest(contamination=0.05, random_state=42)
    daily_totals = daily_sales.sum(axis=1).values.reshape(-1, 1)
    isolation_forest.fit(daily_totals)
    anomalies = isolation_forest.predict(daily_totals)

    # Visualización de anomalías
    plt.figure(figsize=(12, 6))
    plt.plot(daily_sales.index, daily_totals, label='Ventas Totales Diarias')
    plt.scatter(daily_sales.index[anomalies == -1], daily_totals[anomalies == -1], color='red', label='Anomalías', marker='o')
    plt.title("Detección de Anomalías en las Ventas Diarias")
    plt.xlabel("Fecha")
    plt.ylabel("Ventas Totales")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Guardar la segunda gráfica en el mismo directorio
    anomalies_save_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'anomalies.png')
    plt.savefig(anomalies_save_path, format='png')
    plt.close()

    # Fechas con anomalías
    anomalous_dates = daily_sales.index[anomalies == -1]

    # Pasar los datos y las imágenes al template
    context = {
        'daily_sales_plot': '/static/images/grafica.png',  # Ruta a la primera gráfica
        'anomalies_plot': '/static/images/anomalies.png',  # Ruta a la segunda gráfica
        'anomalous_dates': anomalous_dates
    }

    return render(request, 'anomalias.html', context)
