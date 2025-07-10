from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from src.services import verify_token
from src.routes import router
from src.auth import auth_router
from typing import Callable, Awaitable
from src.database import initialize_engine, create_db_and_tables
# from contextlib import asynccontextmanager
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn
import sys
import os
from pathlib import Path

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     initialize_engine()
#     create_db_and_tables()
#     yield


app = FastAPI(
    swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}},
    # lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173" , "http://localhost:8000"],  # Use your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(router)

class DBPath(BaseModel):
    path: str

@app.post("/db-path")
async def set_db_path(body: DBPath):
    try:
        initialize_engine(body.path)
        create_db_and_tables()
        return {"message": f"Database initialized successfully at {body.path}"}
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

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

# Then modify your static files mounting:
base_path = Path(get_base_path())
static_path = base_path / 'static'

app.mount("/static", StaticFiles(directory=static_path), name="static")

# List of your frontend HTML files
FRONTEND_PAGES = {
    "": "index.html",
    "dashboard": "dashboard.html",
    "signup": "signup.html",
}

@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    print(full_path)
    # Check if the path matches one of our frontend pages
    if full_path in FRONTEND_PAGES:
        file_path = static_path / FRONTEND_PAGES[full_path]
        if file_path.exists():
            return FileResponse(file_path)
    
    # Check if the request is for a static file (like JS or CSS)
    static_file = static_path / full_path
    if static_file.exists() and static_file.is_file():
        return FileResponse(static_file)
    
    # Default to index.html for all other paths (SPA behavior)
    index_file = static_path / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    
    return {"message": "Frontend not built"}

# if __name__ == "__main__":
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
