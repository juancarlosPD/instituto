@echo off
cd /d "%~dp0"
entorno\Scripts\python.exe manage.py preparar_album
if errorlevel 1 (
 echo No se ha podido preparar el album. Revisa el error anterior.
 pause
 exit /b 1
)
echo Ahora puedes incluir album_publicado al actualizar GitHub.
pause
