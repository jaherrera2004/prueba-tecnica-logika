FROM python:3.11.8

# Establecer directorio de trabajo
WORKDIR /code

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*
# Actualizar pip, setuptools y wheel
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiar archivos de configuración de Alembic
COPY alembic.ini .

# Copiar el código de la aplicación
COPY ./app /code/app

# Copiar el script de inicio
COPY entrypoint.sh .

# Dar permisos de ejecución al script
RUN chmod +x entrypoint.sh

# Exponer el puerto
EXPOSE 8000

# Ejecutar el script que corre migraciones y luego inicia la app
CMD ["./entrypoint.sh"]
