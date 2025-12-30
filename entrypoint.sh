#!/bin/bash
# Script para ejecutar migraciones de Alembic en Docker

echo "Esperando a que PostgreSQL esté listo..."
sleep 5

echo "Ejecutando migraciones de Alembic..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "Migraciones aplicadas exitosamente"
else
    echo "Error al aplicar migraciones"
    exit 1
fi

echo "Iniciando aplicación FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
