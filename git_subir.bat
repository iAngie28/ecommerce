@echo off
setlocal
set /p msg="Mensaje del commit: "
if "%msg%"=="" (
    echo El mensaje no puede estar vacio.
    exit /b 1
)
git add .
git commit -m "%msg%"
git push -u origin config-VPS
echo.
echo [EXITO] Cambios subidos a la rama config-VPS
endlocal
