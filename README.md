# QRBox

**QRBox** es una aplicación de escritorio para Windows desarrollada por **NICOLUSA**. Permite generar códigos QR a partir de enlaces y texto, previsualizarlos y guardarlos como imágenes PNG.

## Funciones del MVP
- QR para enlaces.
- QR para texto.
- Vista previa.
- Exportación PNG.
- Generación local: el contenido no se envía a servidores.

## Requisitos
- Windows 10/11
- Python 3.10 o posterior para ejecutar desde código.

## Ejecutar desde código
```bash
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r requirements.txt
python src/main.py
```

## Crear ejecutable
Haz doble clic en `build.bat`. El resultado estará en `dist/QRBox.exe`.

## Estado
MVP inicial en desarrollo. Antes de distribuir, probar el ejecutable en una instalación limpia de Windows.
