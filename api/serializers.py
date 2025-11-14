from rest_framework import serializers
from .models import UsuarioPerfil

class UsuarioPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioPerfil
        fields = [
            "id",
            "nombre",
            "email",
            "password",
            "edad",
            "profesion",
            "cosas_que_le_gustan",
            "cosas_que_le_afectan",
            "hobbies",
            "deportes",
            "musica",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"required": True},
            "nombre": {"required": True},
        }
