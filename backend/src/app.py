from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from services import verify_token
from routes import router
from auth import auth_router
from typing import Callable, Awaitable
from database import initialize_engine, create_db_and_tables

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173" , "http://localhost:8000"],  # Use your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(router)

@app.post("/db-path")
async def initialize_db(db_path: str):
    try:
        initialize_engine(db_path)
        create_db_and_tables()
        return {"message": f"Database initialized successfully at {db_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.middleware("http")
async def auth_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    if request.method == "OPTIONS":
        response = await call_next(request)
        return response
    
    if request.url.path.startswith("/resignees"):
        token = request.cookies.get("access_token")
        if not token or not await verify_token(token):
            print('ohno')
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    return await call_next(request)