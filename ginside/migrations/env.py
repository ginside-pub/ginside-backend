from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from ginside.core.config import cfg
from ginside.core.postgres import metadata
from ginside import models  # noqa: F401


alembic_config = context.config

if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

target_metadata = metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """

    context.configure(
        url=cfg.database.get_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """

    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
        url=cfg.database.get_url(),
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
