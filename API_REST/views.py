from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Estudiante, GrupoXEstudiante, Seguimiento, Categoria
from .serializers import EstudianteSerializer, GrupoXEstudianteSerializer, SeguimientoSerializer
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

#Cada clase significa una vista, heredan de APIView para implementar los metodos HTTP (Get, Post , Put, Delete)
class Estudiantes(APIView):
    #Método GET, no se reciben parametros.
    def get(self, request):
        #Se toman todos los estudiantes de la base de datos.
        listaEstudiantes = Estudiante.objects.all()
        #Se deben convertir los datos a un formato JSON. Se pasa la lista y el many para indicar la cantidad
        serializer = EstudianteSerializer(listaEstudiantes, many=True)
        #Se retorna la respuesta con los datos y el código HTTP 200
        return Response({"status": status.HTTP_200_OK, "entity": serializer.data, "error":""},\
         status=status.HTTP_200_OK)
    
    #Método POST, se recibe parametro desde el body
    def post(self, request):
        #Se intentan tomar los datos que se requieren para el query
        try:
            #Se toman todos los datos del resquest
            data = request.data
            #Se accede al campo grupo del JSON
            grupo = data['grupo']
            #Se toma el grupo de la base de datos. Filter es una condición, en los parentesis
            #va la condición del atributo de la tabla.
            listagrupo = GrupoXEstudiante.objects.filter(grupo_id=grupo)

            listaEstudiantes = Estudiante.objects.filter(grupoxestudiante__in=(listagrupo))
            serializer = EstudianteSerializer(listaEstudiantes, many = True)
            return Response({"status": status.HTTP_200_OK, "entity":serializer.data, "error": ""},\
            status=status.HTTP_200_OK)

        except KeyError:
            #Si no es posible obtener los datos desde el Request
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error": "Campos ingresador de forma incorrecta"},\
             status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            #Si no existen datos en la base de datos.
            return Response({"status": status.HTTP_404_NOT_FOUND, "entity":"", "error": "No hay datos"},\
             status= status.HTTP_404_NOT_FOUND)

class Seguimientos(APIView):
    #Método POST, se recibe parametro desde el body
    #Se usa para traer los datos comportamentales
    def post(self, request):
        try:
            #Se toman todos los datos del resquest
            data = request.data 
            id_estudiante = data['id_estudiante']
            tipo_categoria = data['tipo_categoria']
            fecha = data['fecha']
            #Con cada argumento en Values se toma una columna en especifico.
            #Sucede que las tablas en la relación Many, pueden acceser a su relación One, por medio de 
            #su atributo definido en su modelo, en este caso categoria.
            #Cada , es un AND en un Where
            #Los __ son para acceder a las columnas del Modelo referenciado por la varible categoria
            seguimientos = Seguimiento.objects.values('categoria__id','categoria__nombre','categoria__icono','acumulador')\
            .filter(categoria_id__tipo=tipo_categoria, grupoxestudiante_id__estudiante=id_estudiante, fecha=fecha)

            #Se retorna los datos recolectados y el status 200
            return Response({"status": status.HTTP_200_OK, "entity":seguimientos, "error": ""},\
             status=status.HTTP_200_OK)
        except KeyError:
            #Si no es posible obtener los datos desde el Request
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity": "", "error":"Datos ingresador de forma incorrecta"},\
             status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            #Si no existen datos en la base de datos.
            return Response({"status": status.HTTP_404_NOT_FOUND, "entity":"", "error":"No hay datos en la base de datos"},\
             status= status.HTTP_404_NOT_FOUND)

    #Se usa para actualizar un solo dato comportamentales
    def put(self, request):
        try:
            #Se toman todos los datos del resquest
            data = request.data
            id_estudiante = data['id_estudiante']
            id_categoria = data['id_categoria']
            fecha = data['fecha']
            acumulador = data['acumulador']

            #Se busca un objeto que cumpla las caracteristicas del filter. Cada , es un AND
            #Se ejecuta el update, y en sus parametros van las columnas a actulizar
            Seguimiento.objects.filter(categoria_id__id=id_categoria, grupoxestudiante_id__estudiante=id_estudiante, fecha=fecha)\
                .update(acumulador=acumulador)
            #Se retorna los datos recolectados y el status 200
            return(Response({"status": status.HTTP_200_OK, "entity": "", "error":""},status=status.HTTP_200_OK))
        except KeyError:
             #Si no es posible obtener los datos desde el Request
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error":"No se puede actualizar. Datos ingresados de forma incorrecta"},\
             status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            #Si no existen datos en la base de datos.
            return Response({"status": status.HTTP_404_NOT_FOUND, "entity": "", "error":"No se puede acceder a la base de datos"},\
             status= status.HTTP_404_NOT_FOUND)
