from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from .models import Estudiante, GrupoXEstudiante, Seguimiento, Categoria
from .serializers import EstudianteSerializer, GrupoXEstudianteSerializer
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

#Cada clase significa una vista, heredan de APIView para implementar los metodos HTTP (Get, Post , Put, Delete)
class Estudiantes(APIView):
    def get(self, request):
        listaEstudiantes = Estudiante.objects.all()
        serializer = EstudianteSerializer(listaEstudiantes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        try:
            data = request.data
            grupo = data['grupo']
            listagrupo = GrupoXEstudiante.objects.filter(grupo_id=grupo)
            listaEstudiantes = Estudiante.objects.filter(grupoxestudiante__in=(listagrupo))
            serializer = EstudianteSerializer(listaEstudiantes, many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except KeyError:
            return Response({"msg": "Error: No se encuentra el campo grupo"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"msg": "No hay datos en la base de datos"}, status= status.HTTP_404_NOT_FOUND)

class Seguimientos(APIView):
    def post(self, request):
        try:
            data = request.data 
            id_estudiante = data['id_estudiante']
            tipo_categoria = data['tipo_categoria']
            seguimientos = Seguimiento.objects.values('categoria__id','categoria__nombre','categoria__icono','acumulador')\
            .filter(categoria_id__tipo=tipo_categoria, grupoxestudiante_id__estudiante=id_estudiante)
            return Response(seguimientos, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"msg": "Error: No se encuentra el campo grupo"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"msg": "No hay datos en la base de datos"}, status= status.HTTP_404_NOT_FOUND)