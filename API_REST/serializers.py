from rest_framework import serializers
from .models import *

#Una vez definido los modelos, se deben generar los serializadores, es decir, una clase
#Encargada de devolver los datos de la clase en formatos espciales como JSON
class ProfesorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesor
        fields= ('id', 'nombres', 'apellidos', 'correo', 'sexo_biologico')

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo
        fields = ('id', 'grado', 'consecutivo', 'ano')

class ProfesorXGrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfesorXGrupo
        fields = ('profesor', 'grupo')

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = ('id', 'nombres', 'apellidos', 'sexo_biologico', 'descripcion')

class GrupoXEstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoXEstudiante
        fields = ('grupo', 'estudiante')

class CategoriaSerializar(serializers.ModelSerializer):
    class Meta: 
        model = Categoria
        fields = ('id', 'subcategoria', 'nombre', 'tipo', 'icono')

class SeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seguimiento
        fields = ('categoria', 'grupoxestudiante', 'fecha', 'acumulador')

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = ('fecha', 'grupoxestudiante', 'asistencia')