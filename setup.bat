@echo off
REM Script de instalacion y ejecucion - Windows PowerShell
REM ============================================================================

cls
echo.
echo ============================================================================
echo  INTELIGENCIA EN OPERACIONES - Setup & Run
echo ============================================================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en PATH
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Menu
echo Opciones:
echo.
echo  1) Instalar dependencias (solo primera vez)
echo  2) Verificar sistema (diagnóstico)
echo  3) Regenerar ChromaDB
echo  4) Ejecutar interfaz web (Streamlit)
echo  5) Ejecutar script de prueba
echo  6) Todo (instalar + diagnosticar)
echo.
echo ============================================================================
echo.

set /p opcion="Selecciona una opción (1-6): "

if "%opcion%"=="1" (
    echo.
    echo Instalando dependencias...
    pip install -r requirements.txt
    echo.
    echo ✅ Instalación completada
    pause
)

if "%opcion%"=="2" (
    echo.
    echo Ejecutando diagnóstico...
    python verificador.py --diagnose
    echo.
    pause
)

if "%opcion%"=="3" (
    echo.
    echo Regenerando ChromaDB...
    python verificador.py --regenerate-db
    echo.
    pause
)

if "%opcion%"=="4" (
    echo.
    echo Iniciando interfaz web...
    streamlit run app_ui.py
)

if "%opcion%"=="5" (
    echo.
    echo Ejecutando pruebas...
    python prueba.py
    echo.
    pause
)

if "%opcion%"=="6" (
    echo.
    echo Instalando dependencias...
    pip install -r requirements.txt
    echo.
    echo ✅ Instalación completada
    echo.
    echo Ejecutando diagnóstico...
    python verificador.py --diagnose
    echo.
    pause
)

echo Opción inválida
pause
