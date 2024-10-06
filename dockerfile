# Usar la imagen oficial de Python 3.10
FROM python:3.10-slim

# Establecer la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos a la imagen
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el contenido del directorio actual al contenedor
COPY . .

# Exponer el puerto en el que correrá la aplicación (ajústalo según tu necesidad)
EXPOSE 8000

# Definir el comando por defecto para ejecutar la aplicación
CMD ["python", "main.py"]