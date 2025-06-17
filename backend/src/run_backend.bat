cd /d "/home/skiym/repos/aub-resignee-tracker/backend/src"
uvicorn app:app --host 0.0.0.0 --port 8000 --reload --ssl-keyfile=key.pem --ssl-certfile=cert.pem
