from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Alumno, FotoAlumno


def inicio(request: HttpRequest) -> HttpResponse:
    return render(request, "historia/inicio.html", {"alumnos": Alumno.objects.prefetch_related("fotos").all()})


def foto_alumno(request, pk, epoca):
    alumno = get_object_or_404(Alumno, pk=pk)
    campos = {"instituto": alumno.foto_instituto, "actualidad": alumno.foto_actual}
    if epoca.isdecimal():
        foto = get_object_or_404(FotoAlumno, alumno=alumno, pk=int(epoca)).imagen
    else:
        foto = campos.get(epoca)
    if not foto:
        raise Http404("Fotografía no disponible")
    try:
        response = FileResponse(foto.open("rb"))
    except FileNotFoundError:
        raise Http404("Fotografía no disponible")
    response["X-Content-Type-Options"] = "nosniff"
    return response
