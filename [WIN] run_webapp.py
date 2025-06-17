import subprocess
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def run_backend():
    backend_dir = os.path.join(PROJECT_ROOT, "backend", "src")
    backend_script = os.path.join(backend_dir, "run_backend.bat")
    subprocess.Popen([
        "cmd.exe", "/c", "start", "cmd.exe", "/k", backend_script
    ])

def run_frontend():
    frontend_dir = os.path.join(PROJECT_ROOT, "frontend")
    frontend_script = os.path.join(frontend_dir, "run_frontend.bat")
    subprocess.Popen([
        "cmd.exe", "/c", "start", "cmd.exe", "/k", frontend_script
    ])

def create_command_scripts():
    backend_dir = os.path.join(PROJECT_ROOT, "backend", "src")
    frontend_dir = os.path.join(PROJECT_ROOT, "frontend")

    backend_script = os.path.join(backend_dir, "run_backend.bat")
    frontend_script = os.path.join(frontend_dir, "run_frontend.bat")

    with open(backend_script, "w") as f:
        f.write(f'cd /d "{backend_dir}"\n')
        f.write('uvicorn app:app --host 0.0.0.0 --port 8000 --reload --ssl-keyfile=key.pem --ssl-certfile=cert.pem\n')
    with open(frontend_script, "w") as f:
        f.write(f'cd /d "{frontend_dir}"\n')
        f.write('npm run dev\n')

if __name__ == "__main__":
    create_command_scripts()
    run_backend()
    run_frontend()
    print("Backend and frontend servers are starting in new Command Prompt windows.")