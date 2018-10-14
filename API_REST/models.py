from django.db import models
from datetime import date

# Create your models here.
#En esta clase se generan los modelos que estarán en la base de datos

#Las clases siempre heredan de Model, el cual es el ayudante de Django

#Cada campo tiene el tipo definido, se recomienda lectura oficial de la documentación
#           Disponible en: https://docs.djangoproject.com/en/2.0/topics/db/models/


class Profesor(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    correo = models.EmailField(max_length=253)
    contrasena = models.CharField(max_length=255)
    #1. Cedula Ciudadania 2. Cedula Extranjera
    tipo_documento = models.PositiveIntegerField(default=1)
    numero_documento = models.CharField(max_length=30)
    #1. Masculino   2. Femenino
    sexo_biologico = models.PositiveIntegerField(default=1)

    def __str__(self):
            return self.nombres + " " + self.apellidos

class Grupo(models.Model):
    id = models.AutoField(primary_key=True)
    grado = models.CharField(max_length=50)
    consecutivo = models.CharField(max_length=4, default="NA")
    ano = models.SmallIntegerField(default=2018)

    def __str__(self):
        return self.grado + " - " + self.consecutivo + " " + str(self.ano)

class ProfesorXGrupo(models.Model):
    profesor = models.ForeignKey('Profesor', on_delete = models.CASCADE)
    grupo = models.ForeignKey('Grupo', on_delete = models.CASCADE)

    def __str__(self):
            return str(self.profesor) + ' ' +  str(self.grupo)

class Estudiante(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    #1. Masculino   2. Femenino
    sexo_biologico = models.PositiveIntegerField(default=1)
    descripcion =  models.TextField(null = True, blank=True)

    def __str__(self):
        return self.nombres + " " + self.apellidos

class GrupoXEstudiante(models.Model):
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE)
    fila = models.IntegerField(default = -1)
    columna = models.IntegerField(default = -1)

    def __str__(self):
            return str(self.estudiante)+ ' ' +str(self.grupo)

#Aquí existe una relación One to Many hacia la misma clase
#Se logra colocando la palabra self al modelo de referencia
class Categoria(models.Model):
    id = models.AutoField(primary_key = True)
    padre = models.ForeignKey('self', on_delete=models.SET_NULL, null = True, blank=True)
    nombre = models.CharField(max_length = 75)
    #Se usa para especificar si es Comportamental, Cognitivo
    #1 Comportamental 2 Cognitivo
    tipo = models.PositiveIntegerField(default=1)
    icono = models.CharField(null=True, max_length=200, blank=True)
    descripcion = models.CharField(null=True, max_length=200, blank=True)

    def __str__(self):
        if(self.tipo == 1):
            return self.nombre + " - " + "Comportamental"
        else:
            return self.nombre + " - " + "Cognitiva"

class Seguimiento(models.Model):
    categoria = models.ForeignKey('Categoria', null = True, on_delete=models.CASCADE)
    grupoxestudiante = models.ForeignKey('GrupoXEstudiante', on_delete = models.CASCADE)
    fecha = models.DateField(default=date.today)
    acumulador = models.PositiveIntegerField(default=0)

    def __str__(self):
            return str(self.categoria) + ' ' + str(self.grupoxestudiante) + ' ' + str(self.fecha)

class Asistencia(models.Model):
    fecha = models.DateField(default = date.today)
    grupoxestudiante = models.ForeignKey('GrupoXEstudiante', on_delete=models.CASCADE)
    #1. Asistío 2. Llego tarde 3. No Asistio
    asistencia = models.PositiveIntegerField(default=1)

    def __str__(self):
        if(self.asistencia == 1):
            return str(self.grupoxestudiante) + " Asistio el día " + str(self.fecha)
        elif(self.asistencia == 2):
            return str(self.grupoxestudiante) + " Llego tarde el día " + str(self.fecha)
        else:
            return str(self.grupoxestudiante) + " No asistio el día " + str(self.fecha)
