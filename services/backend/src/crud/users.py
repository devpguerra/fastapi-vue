from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Users
from src.schemas.token import Status  # NEW
from src.schemas.users import UserOutSchema

from datetime import datetime
import uuid
from src.auth.users import send_confirmation_email


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user) -> UserOutSchema:
    user.password = pwd_context.encrypt(user.password)
    if(user.auth_provider is None):
        user.auth_provider = "local"

    # Step 1: Generate confirmation token
    confirmation_token = str(uuid.uuid4())

    try:
        user_obj = await Users.create(
            **user.dict(exclude_unset=True),
            confirmation_token=confirmation_token,
            token_created_at=datetime.utcnow(),
            is_confirmed=False
        )
    except IntegrityError as e:
        error_str = str(e)
        # Try to determine which field caused the IntegrityError
        if 'username' in error_str:
            raise HTTPException(status_code=400, detail="That username is already taken.")
        elif 'email' in error_str:
            raise HTTPException(status_code=400, detail="That email is already registered.")
        else:
            raise HTTPException(status_code=400, detail="Username or email already exists.")
        
    send_confirmation_email(user_obj.email, confirmation_token)


    return await UserOutSchema.from_tortoise_orm(user_obj)


async def delete_user(user_id, current_user) -> Status:  # UPDATED
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    if db_user.id == current_user.id:
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")  # UPDATED

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")

async def get_user_by_email(email: str):
    return await Users.get_or_none(email=email)