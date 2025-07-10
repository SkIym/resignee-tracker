from src.app import app
import uvicorn
import sys
import threading
import webview
import ctypes

def set_window_title(title):
    if sys.platform == 'win32':
        ctypes.windll.kernel32.SetConsoleTitleW(title)

def run_fastapi():
    uvicorn.run("src.app:app", host="127.0.0.1", port=8000)

# ✅ PyWebView API to get full file path
class API:
    def select_file(self):
        # ✅ Correct way to open the file dialog from the main window context
        window = webview.windows[0]  # Assume there's only one window
        result = window.create_file_dialog(
            webview.OPEN_DIALOG,
            file_types=('DB Files (*.db)',)
        )
        return result[0] if result else None

if __name__ == "__main__":
    set_window_title("AUB Resignee Tracker")

    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    api = API()

    window = webview.create_window(
        "AUB Resignee Tracker",
        "http://localhost:8000",
        width=1200,
        height=800,
        min_size=(800, 600),
        confirm_close=True,
        js_api=api
    )

    webview.start(gui='edgechromium', debug=True, http_server=True)
