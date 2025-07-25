from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, constr, EmailStr, validator
from typing import Optional


from src.database.models import Users

UserOutSchema = pydantic_model_creator(
    Users, name="UserOut", exclude=["password", "created_at", "modified_at"]
)
UserDatabaseSchema = pydantic_model_creator(
    Users, name="User", exclude=["created_at", "modified_at"]
)

class UserInSchema(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: Optional[str] = None
    auth_provider: Optional[str] = None

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one number.")
        return value

class ResetPasswordSchema(BaseModel):
    token: str
    new_password: constr(min_length=6)

class ForgotPasswordSchema(BaseModel):
    email: EmailStr