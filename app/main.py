from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from app.api import auth_api, task_api
from app.core.handlers import validation_exception_handler, http_exception_handler, general_exception_handler

app = FastAPI(
    title="Prueba Técnica Logika API",
    description="API desarrollada con FastAPI",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar manejadores de excepciones globales
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Prueba Técnica Logika",
        "status": "active"
    }


@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la API"""
    return {"status": "healthy"}

# Registrar routers
app.include_router(auth_api.router, prefix="/api/v1/auth", tags=["users"])
app.include_router(task_api.router, prefix="/api/v1/tasks", tags=["tasks"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
