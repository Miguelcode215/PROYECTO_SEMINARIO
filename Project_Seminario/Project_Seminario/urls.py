"""
URL configuration for Project_Seminario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Anomalias.views import Deteccion_Anomalias
from django.conf import settings
from django.conf.urls.static import static
from Clasificacion.views import image_classification_view
from Productos_CH.views import mostrar_graficos
from Variabilidad.views import analisis_ventas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('anomalias', Deteccion_Anomalias, name='anomalias'),
    path('clasificacion', image_classification_view, name='clasificacion'),
    path('graficosCH', mostrar_graficos, name='graficosCH'),
    path('variabilidad', analisis_ventas, name='variabilidad'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)