from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os

# Ensure the app directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your models so Alembic knows about them
from app.models import device, location, user, assignment, maintenance_log
from app.database import Base

# Alembic Config object: pulls values from alembic.ini
config = context.config

# Configure logging using the .ini file
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tell Alembic which metadata to use for autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This mode does not require a database connection.
    Alembic will generate raw SQL migration scripts.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    Alembic connects to the database and applies migrations directly.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# Decide whether to run online or offline
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
