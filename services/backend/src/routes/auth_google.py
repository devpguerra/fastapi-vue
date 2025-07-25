from fastapi import Request, HTTPException, APIRouter
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import os

from src.auth.jwthandler import create_access_token
from src.crud import users as crud_users  # adjust path if needed
from src.schemas.users import UserInSchema

router = APIRouter()

config = Config(environ=os.environ)
oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={"scope": "openid email profile"},
)

@router.get("/login/google")
async def login_via_google(request: Request):
    redirect_uri = f"{os.getenv('BASE_URL')}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_data = await oauth.google.get("userinfo", token=token)
    user_info = user_data.json()

    if not user_info or "email" not in user_info:
        raise HTTPException(status_code=400, detail="Google login failed")
    


    email = user_info["email"]
    full_name = user_info.get("name", "")

    user = await crud_users.get_user_by_email(email)

    if user:
        # 🔒 SECURITY CHECK: make sure Google login is allowed
        if "google" not in user.auth_provider:
            error_msg = "This account was created with a password. Google login is not enabled."
            return RedirectResponse(
                url=f"{os.getenv('VUE_APP_URL')}/error?msg={error_msg}"
            )
    else:
        # Create new user for Google
        new_user_data = UserInSchema(
            username=email,
            email=email,
            full_name=full_name,
            password="Google_oauth_dummy_12345",  # placeholder
            auth_provider="google"
        )
        user = await crud_users.create_user(new_user_data)

    access_token = create_access_token(data={"sub": user.username})

    response = RedirectResponse(url=f"{os.getenv('VUE_APP_URL')}/dashboard")  # Or your Vue app
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite="Lax",
        secure=False,
        max_age=1800,
    )
    return response