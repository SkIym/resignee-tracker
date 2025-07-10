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
    )


# 🔹 Define PyWebView API class to expose file selection
class API:
    def select_file(self):
        result = webview.create_file_dialog(
            webview.OPEN_DIALOG,
            file_types=('DB Files (*.db)', 'All Files (*.*)')
        )
        if result:
            return result[0]  # full path to selected file
        return None


if __name__ == "__main__":
    set_window_title("AUB Resignee Tracker")

    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    # Create pywebview window
    window = webview.create_window(
        "AUB Resignee Tracker",
        "http://localhost:8000",
        width=1200,
        height=800,
        min_size=(800, 600),
        confirm_close=True
    )

    # Start pywebview with API exposed to frontend JS
    webview.start(gui='edgechromium', debug=True, http_server=True, api=API())
