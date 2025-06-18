import subprocess
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

def run_backend():
    backend_dir = os.path.join(PROJECT_ROOT, "backend", "src")
    command = (
        'uvicorn app:app --host 0.0.0.0 --port 8000 --reload '
        '--ssl-keyfile=key.pem --ssl-certfile=cert.pem'
    )
    # Open a new Terminal window and run the backend command
    subprocess.Popen([
        "open", "-a", "Terminal",
        f"{backend_dir}/run_backend.command"
    ])

def run_frontend():
    frontend_dir = os.path.join(PROJECT_ROOT, "frontend")
    # Open a new Terminal window and run the frontend command
    subprocess.Popen([
        "open", "-a", "Terminal",
        f"{frontend_dir}/run_frontend.command"
    ])

def create_command_scripts():
    backend_dir = os.path.join(PROJECT_ROOT, "backend", "src")
    frontend_dir = os.path.join(PROJECT_ROOT, "frontend")

    backend_script = os.path.join(backend_dir, "run_backend.command")
    frontend_script = os.path.join(frontend_dir, "run_frontend.command")

    with open(backend_script, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("cd \"$(dirname \"$0\")\"\n")
        f.write("uvicorn app:app --host 0.0.0.0 --port 8000 --reload --ssl-keyfile=key.pem --ssl-certfile=cert.pem\n")
    with open(frontend_script, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("cd \"$(dirname \"$0\")\"\n")
        f.write("npm run dev\n")

    os.chmod(backend_script, 0o755)
    os.chmod(frontend_script, 0o755)

if __name__ == "__main__":
    create_command_scripts()
    run_backend()
    run_frontend()
    print("Backend and frontend servers are starting in new Terminal windows.")