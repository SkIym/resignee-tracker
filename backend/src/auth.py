from fastapi import APIRouter, HTTPException, Form, Depends
from datetime import datetime
from sqlmodel import Session
from fastapi.responses import Response
from database import get_engine
from datetime import timedelta
import jwt
import os
from fastapi.requests import Request
from models import Account

auth_router = APIRouter(
    tags=["auth"]
)

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

from sqlmodel import Session, select
from models import Account  # Assuming you have an Account model defined

@auth_router.post("/login")
async def login(
    response: Response, 
    username: str = Form(...), 
    password: str = Form(...),
    session: Session = Depends(get_session)):
    """
    Login endpoint for Account table.
    """
    try:
        # Query the database using SQLModel
        statement = select(Account).where(Account.username == username)
        result = session.exec(statement)
        account= result.first()

        if not account:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Verify password (in a real app, use password hashing!)
        if password != account.password:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Generate JWT token
        token_data = {
            "sub": username,
            "exp": datetime.now() + timedelta(hours=12)
        }

        secret_key = os.getenv("JWT_SECRET_KEY")
        if not secret_key:
            raise ValueError("SECRET_KEY not found in environment variables")

        token = jwt.encode(token_data, secret_key, "HS256")
        
        # Set cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer {token}",
            httponly=True,
            max_age=3600 * 12,
            secure=False,  # For HTTPS, toggle to True. For HTTP, to False
            samesite="lax" # For HTTPS, none. For HTTP, lax
        )

        return {"message": "Login successful"}
        
    except HTTPException as e:
        raise e
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

# @auth_router.post("/accounts")
# async def create_account(
#     username: str = Form(...),
#     password: str = Form(...),
#     confirm_password: str = Form(...)
# ):
#     """
#     Create a new account with encrypted password.
#     Ensures no duplicate usernames and that passwords match.
#     """
#     try:
#         if password != confirm_password:
#             raise HTTPException(status_code=400, detail="Passwords do not match")

#         # Check for duplicate username
#         existing = supabase.table("Accounts") \
#             .select("username") \
#             .eq("username", username) \
#             .execute()
#         if existing.data and len(existing.data) > 0:
#             raise HTTPException(status_code=400, detail="Username already exists")

#         encrypted_password = encrypt_field(password)
#         response = supabase.table("Accounts") \
#             .insert({"username": username, "password": encrypted_password}) \
#             .execute()
#         return {"message": "Account created successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))