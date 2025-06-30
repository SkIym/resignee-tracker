from fastapi import APIRouter, HTTPException, Form
from datetime import datetime
from src.supabase_client import supabase
from fastapi.responses import Response
from datetime import timedelta
from src.crypto_utils import encrypt_field, decrypt_field
import jwt
import os
from fastapi.requests import Request

auth_router = APIRouter(
    tags=["auth"]
)

@auth_router.post("/login")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    """
    Login endpoint for Accounts table.
    """
    try:
        db_response = supabase.table("Accounts") \
            .select("*") \
            .eq("username", username) \
            .execute()
        print(db_response)
        if not db_response.data or len(db_response.data) == 0:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        account = db_response.data[0]  
        get_password = (account["password"])

        if password != get_password:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        token_data = {
            "sub": username,
            "exp": datetime.now() + timedelta(hours=12)
        }

        secret_key = os.getenv("JWT_SECRET_KEY")
        if not secret_key:
            raise ValueError("SECRET_KEY not found in environment variables")

        token = jwt.encode(token_data, secret_key, "HS256")
        
        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True,
            max_age=3600 * 12,
            secure=True,  # For HTTPS, toggle to True. For HTTP, to False
            samesite="none" # For HTTPS, none. For HTTP, lax
        )

        print(response.headers)
        
        return {"message": "Login successful"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@auth_router.get("/check-auth")
async def check_auth(request: Request):
    if not request.cookies.get("access_token"):
        raise HTTPException(status_code=401)
    return {"authenticated": True}

@auth_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
        secure=True,
        samesite="none"
                           
    )
    return {"message": "Successfully logged out"}

@auth_router.post("/accounts")
async def create_account(
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    """
    Create a new account with encrypted password.
    Ensures no duplicate usernames and that passwords match.
    """
    try:
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        # Check for duplicate username
        existing = supabase.table("Accounts") \
            .select("username") \
            .eq("username", username) \
            .execute()
        if existing.data and len(existing.data) > 0:
            raise HTTPException(status_code=400, detail="Username already exists")

        encrypted_password = encrypt_field(password)
        response = supabase.table("Accounts") \
            .insert({"username": username, "password": encrypted_password}) \
            .execute()
        return {"message": "Account created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))