import os
from logging.config import fileConfig
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.models import *

# Load environment variables from .env file
load_dotenv()

# This is the Alembic Config object, which provides access to the values
# within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers if the config file is found.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
# Replace this with the appropriate base class from your app if needed.
target_metadata = Base.metadata

# Fetch database URL from environment variable
database_url = os.getenv("DATABASE_URL")
if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    # Get the database URL from the Alembic config
    url = config.get_main_option("sqlalchemy.url")

    # Configure the migration context for offline mode
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Begin and run the migrations
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Create an engine to connect to the database
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Establish connection to the database
    with connectable.connect() as connection:
        # Configure the migration context with the database connection
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        # Begin and run the migrations
        with context.begin_transaction():
            context.run_migrations()

# Choose whether to run migrations online or offline based on context
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()