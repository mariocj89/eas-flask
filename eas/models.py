"""Models of the objects used in EAS"""
import uuid
import datetime as dt
import json
import random

from sqlalchemy import Column
from sqlalchemy.orm import relationship, foreign
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.types import Integer, String, TIMESTAMP, Unicode, UnicodeText
from sqlalchemy.types import TypeDecorator, JSON as _JSON
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AwareTimestamp(TypeDecorator):
    """A timestamp that always have a tz

    As many databases just store on UTC and strip out tzinfo
    """
    impl = TIMESTAMP

    def process_result_value(self, value, dialect):
        if not value.tzinfo:
            value = value.replace(tzinfo=dt.timezone.utc)
        return value


class JSONText(TypeDecorator):
    """Stores and retrieves JSON as UnicodeText.

    Used as sqlite does not support JSON.

    WARNING: Don't try to modify things on it
    """

    impl = UnicodeText

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


JSON = _JSON().with_variant(JSONText, 'sqlite')


class DrawResult(db.Model):
    __tablename__ = 'draw_result'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4().hex
        self.created = dt.datetime.now(dt.timezone.utc)

    id = Column(String(32), primary_key=True)
    created = Column(AwareTimestamp(timezone=True), unique=True, nullable=False,
                     index=True)
    draw_id = Column(String(32), index=True)
    value = Column(JSON)

    def __repr__(self):
        return "<%s  %r>" % (self.__class__.__name__, self.value)


class DrawBaseModel(db.Model):
    """The basic attributes and functionality for a draw"""
    __abstract__ = True

    _RESULT_LIMIT = 50  # Max number of results to keep

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

    @declared_attr
    def results(cls):
        return relationship(
            DrawResult,
            primaryjoin=lambda: foreign(DrawResult.draw_id) == cls.id,
            order_by=lambda: DrawResult.created.desc(),
        )

    def toss(self):
        """Generates and saves a result"""
        result = self.generate_result()
        assert self.id, "Cannot toss on a non persisted draw"
        self.results.append(DrawResult(
            draw_id=self.id,
            value=result,
        ))
        self.results = self.results[:self._RESULT_LIMIT]
        return result

    def generate_result(self):  # pragma: nocover
        raise NotImplementedError()

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.id)


class RandomNumber(DrawBaseModel):
    __tablename__ = 'random_number'

    range_min = Column(Integer, nullable=False)
    range_max = Column(Integer, nullable=False)

    def generate_result(self):
        random_value = random.randint(self.range_min, self.range_max)
        result = [random_value]
        return result


