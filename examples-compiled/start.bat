@echo off
echo ============================================================
echo    OpenFlex Examples - Quick Start Server
echo ============================================================
echo.
python start.py
if errorlevel 1 (
    echo.
    echo Erro ao executar o servidor.
    echo Certifique-se que o Python 3 esta instalado.
    pause
)
