@echo off
setlocal
cd /d "%~dp0"
echo =====================================
echo             QRBox - Build
echo =====================================
python -m pip install --upgrade pip
if errorlevel 1 goto error
python -m pip install -r requirements.txt pyinstaller
if errorlevel 1 goto error
python -m PyInstaller --clean --noconfirm --onefile --windowed --name QRBox src\main.py
if errorlevel 1 goto error
echo.
echo Build terminado. Ejecutable: dist\QRBox.exe
pause
exit /b 0
:error
echo.
echo Ocurrio un error durante la compilacion.
pause
exit /b 1
