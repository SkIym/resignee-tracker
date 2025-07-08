from src.app import app
import uvicorn
import sys
import os
from pathlib import Path
import webbrowser
import threading
import time
import ctypes

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if getattr(sys, 'frozen', False):
        # Try both MEIPASS and executable directory
        base_path = Path(getattr(sys, '_MEIPASS', Path(sys.executable).parent))
    else:
        base_path = Path(__file__).parent
    
    return str(base_path / relative_path)

def set_window_title(title):
    """Set console title (Windows)."""
    if os.name == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(title)

def open_browser():
    time.sleep(1)
    webbrowser.open("https://localhost:8000")

if __name__ == "__main__":
    set_window_title("AUB Resignee Tracker") 
    threading.Thread(target=open_browser).start()
    
    uvicorn.run(
        "src.app:app",
        host="127.0.0.1",
        port=8000,
        ssl_keyfile=resource_path("key.pem"),
        ssl_certfile=resource_path("cert.pem")
    )