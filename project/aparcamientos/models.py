from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Aparcamiento(models.Model):
    #number == id, no me deja django llamarlo id creo
    number = models.IntegerField()
    nombre = models.CharField(max_length=200, default='', blank = True)
    descripcion = models.TextField(default = '', blank = True)
    accesible = models.BooleanField(default=False)
    url = models.CharField(max_length=200, default='', blank = True)
    via = models.CharField(max_length=100, default='', blank=True)
    localidad = models.CharField(max_length=100, default='', blank=True)
    provincia = models.CharField(max_length=30, default='', blank = True)
    codigo_postal = models.CharField(max_length = 10, default='', blank = True)
    barrio = models.CharField(max_length=200, default='', blank = True)
    distrito = models.CharField(max_length=200, default='', blank = True)
    latitud = models.CharField(max_length=200, default='', blank = True)
    longitud = models.CharField(max_length=200, default='',blank = True)
    telefono = models.CharField(max_length=200, default='', blank = True)
    email = models.CharField(max_length = 200, default = '', blank = True)

    def __str__(self):
        return ("{} {}".format(self.number, self.nombre))

class Usuario(models.Model):
    usuario = models.OneToOneField(User, related_name="usuario")
    aparcamientos = models.ManyToManyField(Aparcamiento, related_name="usuarios")
    size = models.IntegerField(default='1')
    color = models.CharField(max_length=20, default='black')
    fecha = models.DateTimeField(default=timezone.now())
    nombre_pagina = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.usuario.username


class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, null = True)
    aparcamiento = models.ForeignKey(Aparcamiento, null=True, related_name="comentarios")
    texto = models.TextField()
    fecha = models.DateTimeField(default = timezone.now())
    def __str__(self):
        return (self.texto)

class Pagina(models.Model):
    usuario = models.ForeignKey(Usuario)
    nombre = models.CharField(max_length=200, default='')
    enlace = models.CharField(max_length=200, default='')
    def __str__(self):
        return ('Pagina de ')
