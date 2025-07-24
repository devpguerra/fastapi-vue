from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel, constr, EmailStr

from src.database.models import Users


UserInSchema = pydantic_model_creator(
    Users, name="UserIn", exclude_readonly=True
)
UserOutSchema = pydantic_model_creator(
    Users, name="UserOut", exclude=["password", "created_at", "modified_at"]
)
UserDatabaseSchema = pydantic_model_creator(
    Users, name="User", exclude=["created_at", "modified_at"]
)

class ResetPasswordSchema(BaseModel):
    token: str
    new_password: constr(min_length=6)

class ForgotPasswordSchema(BaseModel):
    email: EmailStr