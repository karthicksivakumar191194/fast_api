import grpc
from app.db.database import SessionLocal
from app.models import User
from app.services.grpc.proto import user_service_pb2, user_service_pb2_grpc

class UserService(user_service_pb2_grpc.UserServiceServicer):

    def GetUser(self, request, context):
        with SessionLocal() as db:
            # Query the user from the database
            user = db.query(User).filter(User.id == request.user_id).first()
            if user:
                return user_service_pb2.UserResponse(
                    id=str(user.id),
                    name=user.name,
                    email=user.email
                )
            else:
                # Handle case when the user is not found
                context.set_details("User not found")
                context.set_code(grpc.StatusCode.NOT_FOUND)
                return user_service_pb2.UserResponse()
