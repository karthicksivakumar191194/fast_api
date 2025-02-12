import uvicorn
from app.settings import settings
from app.main import app

# GRPC
import threading
from app.grpc_server import run_grpc_server

# def run():
#     # Start the gRPC server in a separate thread
#     grpc_thread = threading.Thread(target=run_grpc_server)
#     grpc_thread.start()
#
#     # Start FastAPI server without auto-reloading enabled
#     uvicorn.run(app, host="0.0.0.0", port=8001)
#
#     uvicorn app.main:app --host 0.0.0.0 --port 8001
#     uvicorn app.main:app --reload --host 0.0.0.0 --port 8001


def run():
    if settings.environment in ["development", "qa", "production"]:
        uvicorn.run("app.main:app", host="0.0.0.0", port=8001)
    else:
        # local
        uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)

if __name__ == "__main__":
    run()