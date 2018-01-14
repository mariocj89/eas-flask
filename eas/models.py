"""Models of the objects used in EAS"""
import uuid
import datetime as dt

from sqlalchemy import Column
from sqlalchemy.types import Integer, String, TIMESTAMP, Unicode, UnicodeText
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class DrawBaseModel(db.Model):
    """The basic attributes and functionality for a draw"""
    __abstract__ = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4().hex
        self.private_id = uuid.uuid4().hex
        self.created = dt.datetime.now(dt.timezone.utc)

    id = Column(String(32), primary_key=True)
    private_id = Column(String(32), index=True)
    created = Column(TIMESTAMP(timezone=True), unique=True, nullable=False, index=True)
    title = Column(Unicode, nullable=True)
    description = Column(UnicodeText, nullable=True)

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.id)


class RandomNumber(DrawBaseModel):
    __tablename__ = 'random_number'

    range_min = Column(Integer, nullable=False)
    range_max = Column(Integer, nullable=False)

