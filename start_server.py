import uvicorn
from backend.app import app

if __name__ == '__main__':
    print("Launching IR ETA Prototype FastAPI Server on http://127.0.0.1:8000 ...", flush=True)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
