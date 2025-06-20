from src.app import app
import uvicorn
import sys
import os
from pathlib import Path
import webbrowser
import threading
import time


def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def open_browser():
    time.sleep(1)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000)
    