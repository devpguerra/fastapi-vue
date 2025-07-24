from fastapi import APIRouter, HTTPException
from src.auth.users import send_password_reset_email
from src.auth.jwthandler import generate_password_reset_token, verify_password_reset_token
from src.crud.users import get_user_by_email
from src.database.models import Users
from src.schemas.users import ResetPasswordSchema, UserOutSchema, ForgotPasswordSchema
from tortoise.exceptions import DoesNotExist
from passlib.context import CryptContext
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter()

@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordSchema):
    email = data.email
    # 1. Check if email exists in your DB
    user = await get_user_by_email(email)
    if not user:
        # For security, don't reveal if email doesn't exist
        return {"message": "If your email is registered, you'll receive a reset link."}
    
    # 2. Generate password reset token (you can use JWT or UUID)
    token = generate_password_reset_token(user.email)
    
    # 3. Construct reset link (adjust your frontend URL accordingly)
    reset_link = f"{os.getenv('VUE_APP_URL')}/reset-password?token={token}"
    
    # 4. Send the reset email
    send_password_reset_email(to_email=email, reset_link=reset_link)
    
    return {"message": "If your email is registered, you'll receive a reset link."}

@router.post("/reset-password")
async def reset_password(data: ResetPasswordSchema):
    email = verify_password_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    try:
        user = await Users.get(email=email)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = pwd_context.hash(data.new_password)
    user.password = hashed_password
    await user.save()

    return {"message": "Password successfully reset"}