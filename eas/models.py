"""Models of the objects used in EAS"""
import uuid
import datetime as dt

from sqlalchemy import Column
from sqlalchemy.types import Integer, String, TIMESTAMP, Unicode, UnicodeText
from sqlalchemy.types import TypeDecorator
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AwareTimestamp(TypeDecorator):
    """A timestamp that always have a tz"""
    impl = TIMESTAMP

    def process_result_value(self, value, dialect):
        if not value.tzinfo:
            value = value.replace(tzinfo=dt.timezone.utc)
        return value


class DrawBaseModel(db.Model):
    """The basic attributes and functionality for a draw"""
    __abstract__ = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4().hex
        self.private_id = uuid.uuid4().hex
        self.created = dt.datetime.now(dt.timezone.utc)
        self.last_updated = self.created

    id = Column(String(32), primary_key=True)
    private_id = Column(String(32), index=True)
    created = Column(AwareTimestamp(timezone=True), index=True)
    last_updated = Column(AwareTimestamp(timezone=True), nullable=False,
                          onupdate=lambda: dt.datetime.now(dt.timezone.utc))
    title = Column(Unicode, nullable=True)
    description = Column(UnicodeText, nullable=True)

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.id)


class ResultBase(db.Model):
    __abstract__ = True
    # TODO: add draw that generated it

    created = Column(AwareTimestamp(timezone=True), unique=True, nullable=False, index=True)

    def __repr__(self):
        #TODO: find better repr. maybe draw and date?
        return "<%s  %r>" % (self.__class__.__name__, self.value)


class RandomNumber(DrawBaseModel):
    __tablename__ = 'random_number'

    range_min = Column(Integer, nullable=False)
    range_max = Column(Integer, nullable=False)



