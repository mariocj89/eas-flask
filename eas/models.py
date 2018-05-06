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


class AwareTimestamp(TypeDecorator):  # pylint: disable=abstract-method
    """A timestamp that always have a tz

    As many databases just store on UTC and strip out tzinfo
    """
    impl = TIMESTAMP

    def process_result_value(self, value, dialect):
        if not value.tzinfo:
            value = value.replace(tzinfo=dt.timezone.utc)
        return value


class JSONText(TypeDecorator):  # pylint: disable=abstract-method
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
    """Model that represents the result of a draw

    Note the value stores in a raw json the result. The actual schema of the
    value depends on the draw.
    """
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
    def results(self):
        """List of results of a given draw

        As draws are defined as subtypes this helps the mapping and return
        them in time order (desc)
        """
        return relationship(
            DrawResult,
            primaryjoin=lambda: foreign(DrawResult.draw_id) == self.id,
            order_by=DrawResult.created.desc,
            cascade="all, delete, delete-orphan",
        )

    def toss(self):
        """Generates and saves a result"""
        result = self.generate_result()
        assert self.id, "Cannot toss on a non persisted draw"
        self.results.insert(0, DrawResult(  # pylint: disable=no-member
            draw_id=self.id,
            value=result,
        ))
        if len(self.results) > self._RESULT_LIMIT:
            # sqlalchemy will delete per 'delete-orphan'
            self.results.pop()  # pylint: disable=no-member
        return result

    def generate_result(self):  # pragma: nocover
        """To be implemented per draw

        Generates a value to be inserted in the draw as a result
        generated a specific time.

        The value needs to be JSON serializable.
        """
        raise NotImplementedError()

    @classmethod
    def get_draw_or_404(cls, id_):
        """Retrieves a draw by either public or private id

        If the id matches no draw, a 404 is raised.
        """
        obj = cls.query.get(id_)
        if not obj:  # Not found, try to search via private_id
            obj = cls.query.filter_by(private_id=id_).first_or_404()
        return obj

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.id)


class RandomNumber(DrawBaseModel):
    """Random number draw

    Given a range, generates a random number
    """
    __tablename__ = 'random_number'

    range_min = Column(Integer, nullable=False)
    range_max = Column(Integer, nullable=False)

    def generate_result(self):
        random_value = random.randint(self.range_min, self.range_max)
        result = [random_value]
        return result
