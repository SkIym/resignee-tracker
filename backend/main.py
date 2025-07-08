from src.app import app
import uvicorn
import sys
import os
from pathlib import Path
import threading
import webview
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

def run_fastapi():
    uvicorn.run(
        "src.app:app",
        host="127.0.0.1",
        port=8000,
        ssl_keyfile=resource_path("key.pem"),
        ssl_certfile=resource_path("cert.pem")
    )

if __name__ == "__main__":
    set_window_title("AUB Resignee Tracker")
    
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Create pywebview window
    window = webview.create_window(
        "AUB Resignee Tracker",
        "https://localhost:8000",
        width=1200,
        height=800,
        min_size=(800, 600),
        confirm_close=True
    )
    
    # Start the webview
    webview.start()