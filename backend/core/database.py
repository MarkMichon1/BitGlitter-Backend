from sqlalchemy import create_engine, Column, Integer, text
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool

from importlib import import_module
import os
from pkgutil import walk_packages

import backend.models

# Database file path
DB_PATH = "config.sqlite3"  # TODO: Integrate into a settings file if needed
DB_URL = f"sqlite:///{DB_PATH}?check_same_thread=False"

# Ensure database file exists
if not os.path.exists(DB_PATH):
    open(DB_PATH, 'a').close()

# Create the engine
engine = create_engine(DB_URL, poolclass=NullPool, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))

# Define the base class for models
Base = declarative_base()


class SQLBaseClass(Base):
    """Base class to remove duplicate boilerplate and simplify database object management."""
    __abstract__ = True
    id = Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()  # Auto-generate tablename based on class name

    @classmethod
    def create(cls, db, **kwargs):
        obj = cls(**kwargs)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db):
        db.delete(self)
        db.commit()

    def save(self, db):
        if self.id is None:
            db.add(self)
        db.commit()
        db.refresh(self)


def enable_wal_mode(db):
    """Enable WAL mode for better write performance in SQLite."""
    db.execute(text("PRAGMA journal_mode=WAL;"))  # Faster writes
    db.execute(text("PRAGMA synchronous=NORMAL;"))  # Speeds up transactions
    db.execute(text("PRAGMA cache_size=-10000;"))  # More cache memory
    db.execute(text("PRAGMA temp_store=MEMORY;"))  # Temp tables in RAM
    db.commit()


def initialize_database():
    # Model load
    import backend.models
    package = backend.models
    for _, module_name, _ in walk_packages(package.__path__, package.__name__ + "."):
        import_module(module_name)

    #DB Load
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    enable_wal_mode(db)

    # Default

    db.close()


def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

