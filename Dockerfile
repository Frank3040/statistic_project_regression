# Usa la imagen oficial de Python como base
FROM python:3.11-slim

# Establece el directorio de trabajo en /app
WORKDIR /app
# Copia los archivos de la aplicación al contenedor
COPY app.py requirements.txt /app/
# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia los archivos de la aplicación al contenedor
COPY static /app/static
COPY scripts /app/scripts
COPY templates /app/templates

# Expone el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]

RUN ls -R /app