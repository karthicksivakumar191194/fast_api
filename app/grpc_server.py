import grpc
from concurrent import futures
import time
from app.services.grpc.proto import user_service_pb2_grpc
from app.services.grpc.user import UserService

def run_grpc_server():
    # Create the gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Register the Service with the server
    user_service_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)

    # Specify the port the server will listen on
    server.add_insecure_port('[::]:50051')

    # Start the server
    server.start()
    print("INFO: gRPC server running on http://0.0.0.0:50051")

    # Keep the server running
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)

