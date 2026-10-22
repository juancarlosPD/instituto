from django.contrib import admin

from .models import Alumno, FotoAlumno


class FotoAlumnoInline(admin.TabularInline):
    model = FotoAlumno
    extra = 1


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    inlines = [FotoAlumnoInline]
    list_display = ["nombre"]
    search_fields = ["nombre"]
    fields = ["nombre", "foto_instituto", "foto_actual"]


admin.site.site_header = "Generación de 1978"
admin.site.site_title = "Administración del álbum"
admin.site.index_title = "Gestionar los compañeros"
