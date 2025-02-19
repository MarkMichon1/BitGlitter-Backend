from sqlalchemy import Boolean, Column, Integer, String

from multiprocessing import cpu_count
import os
from pathlib import Path

from backend.core.database import engine, SQLBaseClass

class ColorSet(SQLBaseClass):
    __tablename__ = 'color_set'
