# aub-resignee-tracker

## Installing dependencies

1. Navigate to the `/frontend` directory:
   ```bash
   cd frontend

2. Install libraries using npm
   ```bash
   npm install

3. Navigate to the `/backend` directory:
   ```bash
   cd frontend

4. Install libraries using pip 
   ```bash
   pip install -r requirements.txt
 
   ```
   If pip is not yet installed, run
   ```bash
   python -m pip install --upgrade pip
   
   ```

## Running the Frontend

1. Navigate to the `/frontend` directory:
   ```bash
   cd frontend

2. Then run:
    ```bash
    npm run dev

## Running the Server (Backend)

1. Navigate to the `/backend` directory:
   ```bash
   cd backend

2. Then run:
    ```bash
    uvicorn app:app

    ```
    To enable auto-reload during development:
    ```bash
    uvicorn app:app --reload

    ```