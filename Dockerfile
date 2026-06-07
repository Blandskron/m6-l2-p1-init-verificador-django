FROM python:3.11-slim

# Evitar que Python escriba archivos .pyc en disco y forzar salida inmediata en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo principal
WORKDIR /app

# Instalar utilidades básicas del sistema (incluido dos2unix para corregir saltos de línea Windows)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar requerimientos de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto al contenedor
COPY . /app/

# Corregir saltos de línea del script entrypoint y darle permisos de ejecución
RUN dos2unix /app/docker-entrypoint.sh \
    && chmod +x /app/docker-entrypoint.sh

# Cambiar el directorio de trabajo donde reside manage.py
WORKDIR /app/init_verificador_django

# Exponer el puerto por defecto de Django
EXPOSE 8000

# Definir el script de punto de entrada
ENTRYPOINT ["/app/docker-entrypoint.sh"]
