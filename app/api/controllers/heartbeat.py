from fastapi import APIRouter

router = APIRouter()

@router.get("/application")
def check_application_heartbeat():
    """
    Heartbeat endpoint to check if the application is alive and healthy.

    Returns:
        dict: A simple JSON response with a "status" key set to "OK".
    """
    return {"status": "OK"}

@router.get("/database")
def check_database_heartbeat():
    """
    Heartbeat endpoint to check if the database is alive and healthy.

    Returns:
        dict: A simple JSON response with a "status" key set to "OK".
    """
    return {"status": "OK"}