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
    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=30)
    sexo_biologico = models.CharField(max_length=25)

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
    profesor = models.ForeignKey('Profesor', null = True, on_delete = models.SET_NULL, blank=True)
    grupo = models.ForeignKey('Grupo', on_delete = models.CASCADE)

    def __str__(self):
            return str(self.profesor) + ' ' +  str(self.grupo)

class Estudiante(models.Model):
    id = models.AutoField(primary_key=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50) 
    sexo_biologico = models.CharField(max_length=25)
    descripcion =  models.TextField(null = True, blank=True)

    def __str__(self):
        return self.nombres + " " + self.apellidos

class GrupoXEstudiante(models.Model):
    grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
    estudiante = models.ForeignKey('Estudiante', null = True, on_delete=models.SET_NULL)

    def __str__(self):
            return str(self.estudiante)+ ' ' +str(self.grupo)

#Aquí existe una relación One to Many hacia la misma clase
#Se logra colocando la palabra self al modelo de referencia
class Categoria(models.Model):
    id = models.AutoField(primary_key = True)
    subcategoria = models.ForeignKey('self', on_delete=models.CASCADE, null = True, blank=True)
    nombre = models.CharField(max_length = 75)
    tipo = models.CharField(max_length = 50)
    icono = models.CharField(null=True, max_length=200, blank=True)

    def __str__(self):
            return self.nombre

class Seguimiento(models.Model):
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    grupoxestudiante = models.ForeignKey('GrupoXEstudiante', on_delete = models.CASCADE)
    fecha = models.DateField(default=date.today)
    acumulador = models.PositiveIntegerField(default=0)

    def __str__(self):
            return str(self.categoria) + ' ' + str(self.grupoxestudiante) + ' ' + str(self.fecha)

class Asistencia(models.Model):
    fecha = models.DateField(default = date.today)
    grupoxestudiante = models.ForeignKey('GrupoXEstudiante', on_delete=models.CASCADE)
    asistencia = models.CharField(max_length=100)