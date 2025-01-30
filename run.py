import uvicorn
from app.main import app

# GRPC
import threading
from app.settings import settings
from app.grpc_server import run_grpc_server

def run():
    # Start the gRPC server in a separate thread
    grpc_thread = threading.Thread(target=run_grpc_server)
    grpc_thread.start()

    # Start FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8001)
    # uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

if __name__ == "__main__":
    run()