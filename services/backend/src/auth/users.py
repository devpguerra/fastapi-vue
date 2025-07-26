from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from tortoise.expressions import Q

from src.database.models import Users
from src.schemas.users import UserDatabaseSchema

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = "dev.patricio.guerra@gmail.com"  # This must be verified in SendGrid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username_or_email: str):
    return await UserDatabaseSchema.from_queryset_single(
         Users.get(Q(username=username_or_email) | Q(email=username_or_email))
    )


async def validate_user(user: OAuth2PasswordRequestForm = Depends()):
    try:
        """ Im sending either username or email inside the user.username field """
        db_user = await get_user(user.username)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return db_user

def send_password_reset_email(to_email: str, reset_link: str):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="Your Password Reset Request",
        html_content=f"""
        <p>Hi,</p>
        <p>You requested a password reset. Click the link below to reset your password:</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <p>If you didn't request this, just ignore this email.</p>
        """
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email: {e}")


def send_confirmation_email(to_email: str, token: str):
    confirm_url = f"{os.getenv('VUE_APP_URL')}/confirm-email?token={token}"

    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject="Confirm your account",
        html_content=f"""
            <p>Welcome! Please confirm your email by clicking the link below:</p>
            <a href="{confirm_url}">Confirm Email</a>
        """
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print("SendGrid error:", e)
        raise