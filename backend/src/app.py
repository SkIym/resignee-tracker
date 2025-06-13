from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from services import verify_token
from routes import router
from typing import Callable, Awaitable

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.middleware("http")
async def auth_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]):

    if request.url.path.startswith("/resignees"):
        token = request.cookies.get("access_token")
        if not token or not await verify_token(token):
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    return await call_next(request)
