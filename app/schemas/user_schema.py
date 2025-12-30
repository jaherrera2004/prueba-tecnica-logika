from pydantic import BaseModel, EmailStr, Field, field_validator


# Schema para registro
class UserRegister(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    lastname: str = Field(..., min_length=1, max_length=255)
    email: str
    password: str = Field(..., min_length=6, max_length=72)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) < 1:
            raise ValueError('El nombre es obligatorio y debe tener al menos 1 carácter')
        return v
    
    @field_validator('lastname')
    @classmethod
    def validate_lastname(cls, v):
        if not v or len(v.strip()) < 1:
            raise ValueError('El apellido es obligatorio y debe tener al menos 1 carácter')
        return v
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not v or len(v) < 6:
            raise ValueError('La contraseña debe tener al menos 6 caracteres')
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not '@' in str(v) or not '.' in str(v):
            raise ValueError('Debe proporcionar un email válido')
        return v 
   
   
# Schema para login
class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if not '@' in str(v) or not '.' in str(v):
            raise ValueError('Debe proporcionar un email válido')
        return v


# Schema para respuesta de usuario (sin password)
class UserResponse(BaseModel):
    id: int
    name: str
    lastname: str
    email: str

    class Config:
        from_attributes = True


# Schema para respuesta de autenticación
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse