from sqlmodel import create_engine, SQLModel
import models
from typing import Optional

# Default values
# database.py

from sqlmodel import create_engine, SQLModel
from typing import Optional
import threading

engine = None
sqlite_file_name = None
sqlite_url = None
_engine_lock = threading.Lock()  # for thread-safe engine setup

def get_engine():
    global engine
    if engine is None:
        raise RuntimeError("Database engine not initialized. Call initialize_engine first.")
    return engine

def initialize_engine(db_path: str = "database.db"):
    global engine, sqlite_file_name, sqlite_url
    with _engine_lock:
        sqlite_file_name = db_path
        sqlite_url = f"sqlite:///{sqlite_file_name}"
        engine = create_engine(sqlite_url, echo=True)
    return engine

def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(get_engine())
        print("Database tables created successfully")
    except Exception as e:
        raise Exception(str(e))