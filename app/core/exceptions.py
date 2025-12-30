from fastapi import HTTPException

class ValidationError(HTTPException):
    def __init__(self, detail: str = "Error de validación"):
        super().__init__(status_code=422, detail=detail)

class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Error de autenticación"):
        super().__init__(status_code=401, detail=detail)

class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "No autorizado"):
        super().__init__(status_code=403, detail=detail)

class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(status_code=404, detail=detail)

class InternalServerError(HTTPException):
    def __init__(self, detail: str = "Error interno del servidor"):
        super().__init__(status_code=500, detail=detail)