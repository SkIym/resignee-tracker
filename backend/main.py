from src.app import app
import uvicorn
import sys
import os
from pathlib import Path
import webbrowser
import threading
import time
import ctypes

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def set_window_title(title):
    """Set console title (Windows)."""
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)

def open_browser():
    time.sleep(1)
    webbrowser.open("http://localhost:8000")

if __name__ == "__main__":
    set_window_title("AUB Resignee Tracker") 
    threading.Thread(target=open_browser).start()
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000)
    