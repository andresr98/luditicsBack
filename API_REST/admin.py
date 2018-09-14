from django.contrib import admin
from.models import Estudiante, Categoria, Grupo, GrupoXEstudiante, Seguimiento

# Register your models here.
admin.site.register(Estudiante)
admin.site.register(Categoria)
admin.site.register(Seguimiento)
admin.site.register(Grupo)
admin.site.register(GrupoXEstudiante)