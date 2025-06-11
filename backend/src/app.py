from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase_client import supabase
<<<<<<< HEAD
from datetime import datetime
=======
from routes import router
>>>>>>> 255e889bc1a9904196ebc0e20f2f922b8206e0b7

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": {"theme": "obsidian"}})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/ResignedEmployees")
def get_items():
    try:
        response = supabase.table("ResignedEmployees").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ResignedEmployees")
def create_item(item: dict):
    try:
        response = supabase.table("ResignedEmployees").insert(item).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))