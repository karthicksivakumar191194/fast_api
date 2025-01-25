from logging.config import dictConfig
from app.settings import settings

# Define the logging configuration
log_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # Standard output for info level messages
        'stdout': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
        },
        # Standard error output for error level messages
        'stderr': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'default',
        },
        # File handler for info level logs (fapi_log_access.log)
        'file_stdout': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': settings.log_stdout_filename,
            'formatter': 'default',
        },
        # File handler for error level logs (fapi_log_error.log)
        'file_stderr': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': settings.log_stderr_filename,
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {
            'handlers': ['stdout', 'stderr', 'file_stdout', 'file_stderr'],
            'level': 'DEBUG',  # Captures all messages from DEBUG level and higher
            'propagate': True,
        },
    },
    'formatters': {
        'default': {
            'format': '{asctime} {levelname} {message}',  # Timestamp, log level, message
            'style': '{',
        },
    },
}

# Apply logging configuration
dictConfig(log_config)
