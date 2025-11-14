from django.db import models

class UsuarioPerfil(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    edad = models.IntegerField(null=True, blank=True)
    profesion = models.CharField(max_length=100, blank=True)

    cosas_que_le_gustan = models.TextField(blank=True)
    cosas_que_le_afectan = models.TextField(blank=True)
    hobbies = models.TextField(blank=True)
    deportes = models.TextField(blank=True)
    musica = models.TextField(blank=True)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.email})"
