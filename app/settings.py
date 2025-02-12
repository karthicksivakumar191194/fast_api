from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    app_name: str = 'FastAPI Application'
    debug: bool = False
    environment: str = 'development' # local, development, qa, production
    secret_key: str
    allowed_hosts: List[str] = []

    # PostgreSQL Database
    database_url: str

    # Log file names
    log_stdout_filename: str = 'fapi_log_access.log'
    log_stderr_filename: str = 'fapi_log_error.log'

    # JWT Token settings
    token_expire_seconds: int = 86400  # Expiration time, unit: seconds (86400 = 1 day)
    token_secret_key: str
    token_algorithm: str = 'HS256'

    # Frontend
    frontend_url: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


# Initialize the settings
settings = Settings()