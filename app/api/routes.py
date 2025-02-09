from fastapi import APIRouter
from app.api.controllers.heartbeat import router as heartbeat_router
from app.api.controllers.onboarding.v1.onboarding import router as onboarding_router
# from app.api.controllers.auth.v1.login import router as auth_router
from app.api.controllers.workspace.v1.workspace import router as workspace_router
from app.api.controllers.location.v1.location import router as location_router
# from app.api.controllers.user.v1.user import router as user_router

api_router = APIRouter()

# Include all routes
api_router.include_router(heartbeat_router, prefix="/v1/heartbeat", tags=["Heartbeat"])
api_router.include_router(onboarding_router, prefix="/v1/onboard", tags=["Onboard Account"])
# api_router.include_router(auth_router, prefix="/v1/auth", tags=["Authentication"])
api_router.include_router(workspace_router, prefix="/v1/workspace", tags=["Workspace"])
api_router.include_router(location_router, prefix="/v1/location", tags=["Location"])
# api_router.include_router(user_router, prefix="/v1/user", tags=["User"])
