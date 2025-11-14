# detector/api/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chat/", views.chat_page, name="chat"),
    path("api/login/", views.login_usuario, name="login_api"),
    path("api/registrar/", views.registrar_usuario, name="register_api"),
    path("api/chatbot/", views.chatbot, name="chatbot_api"),
    path("api/usuario/<int:usuario_id>/", views.obtener_usuario, name="obtener_usuario"),
]
