from src.app import app
import uvicorn
import sys
import os
from pathlib import Path

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000)