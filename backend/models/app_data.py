from sqlalchemy import Boolean, Column, Integer, String

from multiprocessing import cpu_count
import os
from pathlib import Path

from backend.core.database import engine, SQLBaseClass

class Settings(SQLBaseClass):

    __tablename__ = 'settings'

    # Processing
    maximum_cpu_cores = Column(Integer, default=cpu_count())
    MAX_SUPPORTED_CPU_CORES = Column(Integer, default=cpu_count())

    # GUI
    show_advanced_state = Column(Boolean, default=True)

    # Read
    delete_on_full_read = Column(Boolean, default=False)

    # Write
    delete_on_write = Column(Boolean, default=False)


class Statistics(SQLBaseClass):
    #todo think about this...
    blocks_wrote = Column(Integer, default=0)
    frames_wrote = Column(Integer, default=0)
    data_wrote_bytes = Column(Integer, default=0)
    blocks_read = Column(Integer, default=0)
    frames_read = Column(Integer, default=0)
    data_read_bytes = Column(Integer, default=0)

    def write_update(self, db, blocks, frames, data):
        self.blocks_wrote += blocks
        self.frames_wrote += frames
        self.data_wrote_bytes += data
        return self.save(db)  # ✅ Method chaining

    def read_update(self, db, blocks, frames, data):
        self.blocks_read += blocks
        self.frames_read += frames
        self.data_read_bytes += data
        return self.save(db)  # ✅ Method chaining

    def return_stats(self):
        return {
            'blocks_wrote': self.blocks_wrote,
            'frames_wrote': self.frames_wrote,
            'data_wrote_bytes': self.data_wrote_bytes,
            'blocks_read': self.blocks_read,
            'frames_read': self.frames_read,
            'data_read_bytes': self.data_read_bytes,
        }

    def clear_stats(self, db):
        """Reset all statistics to zero."""
        self.blocks_wrote = 0
        self.frames_wrote = 0
        self.data_wrote_bytes = 0
        self.blocks_read = 0
        self.frames_read = 0
        self.data_read_bytes = 0
        return self.save(db)

class BaseSession(SQLBaseClass):
    __tablename__ = 'base_session'
    __abstract__ = False
    active = Column(Boolean, default=True)


class WriteSession(SQLBaseClass):
    __tablename__ = 'write_session'
    active = Column(Boolean, default=True)


class ReadSession(SQLBaseClass):
    __tablename__ = 'read_session'
    active = Column(Boolean, default=True)


SQLBaseClass.metadata.create_all(engine)