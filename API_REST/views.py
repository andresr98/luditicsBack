from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Estudiante, GrupoXEstudiante, Seguimiento, Categoria, ProfesorXGrupo, Grupo, Asistencia
from .serializers import EstudianteSerializer
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

#Cada clase significa una vista, heredan de APIView para implementar los metodos HTTP (Get, Post , Put, Delete)
class Estudiantes(APIView):
    #Método GET, no se reciben parametros.
    def get(self, request):
        #Se toman todos los estudiantes de la base de datos.
        id_grupo = request.GET.get('id_grupo',0)

        if(id_grupo == 0):
            listaEstudiantes = Estudiante.objects.values('id', 'nombres', 'apellidos','grupoxestudiante__fila', 'grupoxestudiante__columna', \
            'sexo_biologico', 'descripcion')
            #Se deben convertir los datos a un formato JSON. Se pasa la lista y el many para indicar la cantidad
            return Response({"status": 200, "entity":listaEstudiantes}, status=status.HTTP_200_OK)
        else:
            listagrupo = GrupoXEstudiante.objects.filter(grupo_id=id_grupo)  

            listaEstudiantes = Estudiante.objects.values('id', 'nombres', 'apellidos','grupoxestudiante__fila', 'grupoxestudiante__columna', \
            'sexo_biologico', 'descripcion').filter(grupoxestudiante__in=(listagrupo))

            return Response({"status": status.HTTP_200_OK, "entity":listaEstudiantes, "error": ""},\
            status=status.HTTP_200_OK)
            
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
            .filter(categoria_id__tipo=tipo_categoria, grupoxestudiante_id__estudiante=id_estudiante,fecha=fecha)

            return Response({"status": status.HTTP_200_OK, "entity":seguimientos, "error": ""},\
             status=status.HTTP_200_OK)
        except KeyError:
            #Si no es posible obtener los datos desde el Request
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity": "", "error":"Campos ingresados de forma incorrecta"},\
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

            return(Response({"status": status.HTTP_200_OK, "entity": "", "error":""},status=status.HTTP_200_OK))
        except KeyError:
             #Si no es posible obtener los datos desde el Request
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error":"Campos ingresados de forma incorrecta"},\
             status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            #Si no existen datos en la base de datos.
            return Response({"status": status.HTTP_404_NOT_FOUND, "entity": "", "error":"No se puede acceder a la base de datos"},\
             status= status.HTTP_404_NOT_FOUND)

class Grupos(APIView):
    def get(self,request):
        #En caso de que no exista el parametro profesor, se devuelve un error
        id_profesor = request.GET.get('id_profesor',0)
        if(id_profesor == 0):
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error":"Campos ingresados de forma incorrecta"},\
            status=status.HTTP_400_BAD_REQUEST)
        else:
            #Se filtran los grupos por profesor y se retornan
            grupos = ProfesorXGrupo.objects.values('grupo__id', 'grupo__grado', 'grupo__consecutivo', 'grupo__ano')\
            .filter(profesor_id__id = id_profesor)
            return Response({"status": status.HTTP_200_OK, "entity": grupos, "error":""},status=status.HTTP_200_OK)


#Esta vista se encarga de llenar un seguimiento por cada estudiante
class SeguimientoXEstudiante(APIView):
    def post (self, request):
        try:
            #Se obtienen los datos requeridos en el query
            data = request.data
            id_grupo = data['id_grupo']
            fecha = data['fecha']

            #Se accede a todos los padres de la tabla categoria. Se excluyen los nulos
            padres = Categoria.objects.values('padre_id').distinct().exclude(padre_id__isnull=True)

            #Se obtienen todas las categorias hojas
            categorias = Categoria.objects.values('id').exclude(id__in=(padres))

            #Se obtienen los estudiantes de un grupo
            estudiantes = GrupoXEstudiante.objects.values('estudiante__id').filter(grupo__id=id_grupo)
            for categoria in categorias:
                for estudiante in estudiantes:
                    #Se obtiene el id de la tabla, ya que es autogenerado
                    grupoxest_id = GrupoXEstudiante.objects.values('id').get(grupo = id_grupo, estudiante = estudiante['estudiante__id'])

                    #Se verifica que no exista el dato. En caso afirmativo, se inserta un nuevo registro
                    #En caso contrario solo se dejan sus valores
                    flag = Seguimiento.objects.filter(categoria_id=categoria['id'],fecha=fecha,grupoxestudiante_id=grupoxest_id['id'])
                    if not flag:
                        seguimiento = Seguimiento(categoria_id=categoria['id'],fecha=fecha,acumulador=0,grupoxestudiante_id=grupoxest_id['id'])
                        seguimiento.save()
                    else:
                        flag.update()

            return Response({"status": status.HTTP_201_CREATED, "entity": "Datos ingresados en bd", "error":""},status=status.HTTP_201_CREATED)
        except KeyError:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity": "", "error":"Campos ingresados de forma incorrecta"},status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND, "entity": "", "error":"El objeto no existe"},status=status.HTTP_404_NOT_FOUND)

class Asistencias (APIView):
    def get(self, request):
        #En caso de que no se envie el grupo o la fecha, se retorna error
        id_grupo = request.GET.get('id_grupo', 0)

        if(id_grupo == 0):
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error":"Campos ingresados de forma incorrecta"},\
            status=status.HTTP_400_BAD_REQUEST)
        
        fecha = request.GET.get('fecha', 'default')

        if(fecha == 'default'):
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity":"", "error":"Campos ingresados de forma incorrecta"},\
            status=status.HTTP_400_BAD_REQUEST)

        #Se obtiene el nombre, apellido, id,y el tipo de asistencia donde se filtre por el grupo y la fecha parametro
        asistencias = Asistencia.objects.values('grupoxestudiante__estudiante_id__nombres', 'grupoxestudiante__estudiante_id__apellidos',\
        'grupoxestudiante__estudiante_id__id', 'asistencia', 'grupoxestudiante__fila', 'grupoxestudiante__columna').filter(grupoxestudiante_id__grupo=id_grupo,fecha=fecha)

        return Response({"status": status.HTTP_200_OK, "entity": asistencias, "error":""},status=status.HTTP_200_OK)
        
    def post (self, request):
        #Este metodo llenara toda la asistencia de un grupo, según el numero de estudiantes
        try:
            data = request.data
            id_grupo = data['id_grupo']
            fecha = data['fecha']
            asistencia = 1

            #Se filtran los estudiantes por grupo
            estudiantes = GrupoXEstudiante.objects.values('estudiante__id').filter(grupo__id=id_grupo)

            #Para cada uno de ellos se busca su id en la tabla join y se guarda o se actualiza si existe o no el registro
            for estudiante in estudiantes:
                grupoxest_id = GrupoXEstudiante.objects.values('id').get(grupo = id_grupo, estudiante = estudiante['estudiante__id'])
                
                flag = Asistencia.objects.filter(grupoxestudiante_id=grupoxest_id['id'], fecha = fecha)

                if not flag:
                    asistenciaObjeto = Asistencia(grupoxestudiante_id = grupoxest_id['id'], fecha = fecha, asistencia = asistencia)
                    asistenciaObjeto.save()
                else:
                    flag.update()

            return Response({"status": status.HTTP_201_CREATED, "entity": "Asistencia creada", "error": "" }, status=status.HTTP_201_CREATED)
        
        except KeyError:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity": "", "error":"Campos ingresados de forma incorrecta"},status=status.HTTP_400_BAD_REQUEST)
        
        except ObjectDoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND, "entity": "", "error":"El objeto no existe"},status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        #Acutliza un solo registro
        try:
            data = request.data
            id_grupo = data['id_grupo']
            id_estudiante = data['id_estudiante']
            fecha = data['fecha'] 
            asistencia = data['asistencia']

            #La asistencia solo puede estar en estos tres valores
            if(asistencia != 1 and asistencia != 2 and asistencia != 3):
                return Response({"status": status.HTTP_400_BAD_REQUEST, "entity": "", "error":"Datos ingresados incorrectamente"},status=status.HTTP_400_BAD_REQUEST)

            #Se filtra y se actualiza la columna asistencia
            Asistencia.objects.filter(fecha = fecha, grupoxestudiante_id__estudiante=id_estudiante, grupoxestudiante_id__grupo=id_grupo)\
            .update(asistencia = asistencia)

            return Response({"status": status.HTTP_200_OK, "entity": "Datos actulizados", "error":""},status=status.HTTP_200_OK)

        except KeyError:
            return Response({"status": status.HTTP_400_BAD_REQUEST, "entity": "", "error":"Datos ingresados incorrectamente"},status=status.HTTP_400_BAD_REQUEST)
        
        except ObjectDoesNotExist:
            return Response({"status": status.HTTP_404_NOT_FOUND, "entity": "", "error":"El objeto no existe"},status=status.HTTP_404_NOT_FOUND)