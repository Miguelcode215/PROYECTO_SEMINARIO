import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render
from io import BytesIO
import base64
import os
from django.conf import settings

def mostrar_graficos(request):
    # Cargar el archivo CSV
    filepath = os.path.join(settings.BASE_DIR, 'ventas_agosto-septiembre_2024.xlsx')
    df = pd.read_excel(filepath)

    # Procesar datos como en el código original
    df['Fecha de Venta'] = pd.to_datetime(df['Fecha de Venta'], errors='coerce')
    df['Mes'] = df['Fecha de Venta'].dt.month
    
    # Agrupar datos para los gráficos
    productos_mas_vendidos = df.groupby('Producto').agg({
        'Cantidad Vendida': 'sum',
        'Total Venta (S/)': 'sum'
    }).sort_values(by='Cantidad Vendida', ascending=False)
    
    productos_mas_vendidos.columns = ['Cantidad Total Vendida', 'Ventas Totales (S/)']
    top_productos = productos_mas_vendidos.head(10).reset_index()
    
    # Crear gráficos y guardarlos como imágenes en base64 para mostrarlos en la plantilla
    fig1 = plt.figure(figsize=(10, 6))
    sns.barplot(data=top_productos, x='Cantidad Total Vendida', y='Producto', palette='Blues_r')
    plt.title("Top 10 Productos Más Vendidos (por Cantidad de Unidades)")
    plt.xlabel("Cantidad Total Vendida")
    plt.ylabel("Producto")
    img1 = BytesIO()
    fig1.savefig(img1, format='png')
    img1.seek(0)
    chart1_url = base64.b64encode(img1.getvalue()).decode()

    fig2 = plt.figure(figsize=(10, 6))
    sns.barplot(data=top_productos, x='Ventas Totales (S/)', y='Producto', palette='Reds_r')
    plt.title("Top 10 Productos Más Vendidos (por Ventas Totales en S/)")
    plt.xlabel("Ventas Totales (S/)")
    plt.ylabel("Producto")
    img2 = BytesIO()
    fig2.savefig(img2, format='png')
    img2.seek(0)
    chart2_url = base64.b64encode(img2.getvalue()).decode()

    # Crear gráficos de los top 10 productos para agosto y septiembre
    df_agosto = df[df['Mes'] == 8]
    df_septiembre = df[df['Mes'] == 9]
    top10_agosto = df_agosto.groupby('Producto')['Cantidad Vendida'].sum().nlargest(10).reset_index()
    top10_septiembre = df_septiembre.groupby('Producto')['Cantidad Vendida'].sum().nlargest(10).reset_index()

    fig3, ax = plt.subplots(figsize=(12, 6))
    ancho = 0.4
    indice = range(len(top10_agosto['Producto']))
    ax.bar(indice, top10_agosto['Cantidad Vendida'], width=ancho, label='Agosto', color='blue')
    ax.bar([i + ancho for i in indice], top10_septiembre['Cantidad Vendida'], width=ancho, label='Septiembre', color='green')
    ax.set_xlabel('Producto')
    ax.set_ylabel('Cantidad Vendida')
    ax.set_title('Top 10 Productos Más Vendidos en Agosto y Septiembre')
    ax.set_xticks([i + ancho / 2 for i in indice])
    ax.set_xticklabels(top10_agosto['Producto'], rotation=45, ha='right')
    ax.legend()
    img3 = BytesIO()
    fig3.savefig(img3, format='png')
    img3.seek(0)
    chart3_url = base64.b64encode(img3.getvalue()).decode()

    context = {
        'chart1': chart1_url,
        'chart2': chart2_url,
        'chart3': chart3_url,
    }
    return render(request, 'mostrar_graficos.html', context)
