from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Incluyes las rutas de tu app chatbot
    path('', include('api.urls')),  # o el prefijo que quieras
]
