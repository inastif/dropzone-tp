"""Database engine and session management."""

from collections.abc import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


def make_engine(database_url: str) -> Engine:
    if database_url.startswith("sqlite"):
        options: dict = {"connect_args": {"check_same_thread": False}}
        if ":memory:" in database_url:
            # One shared connection, otherwise each session gets an empty database.
            options["poolclass"] = StaticPool
        return create_engine(database_url, **options)
    return create_engine(database_url, pool_pre_ping=True)


class Database:
    """Holds the engine and the session factory of the running application."""

    def __init__(self, database_url: str) -> None:
        self.engine = make_engine(database_url)
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)

    def create_schema(self) -> None:
        Base.metadata.create_all(self.engine)

    def session(self) -> Iterator[Session]:
        with self.session_factory() as session:
            yield session
