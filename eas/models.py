"""Models of the objects used in EAS"""
import uuid
import datetime as dt

import sqlalchemy
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, TIMESTAMP, Unicode
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def _positive_number(field_name):
    return sqlalchemy.CheckConstraint(
        f'{field_name} > 0',
        name=f"{field_name}_positive",
    )


class SQLFactory:
    """Mixing to add a method to create object on db

    To be applied to a Model class
    """
    @classmethod
    def create(cls, **kwargs):
        """Creates an object and commits it

        @PRE: There is no ongoing transaction or behaviour is undefined
        """
        obj = cls(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj


class DrawBaseModel(db.Model):
    """The basic attributes and functionality for a draw"""

    __abstract__ = True

    id = Column(String(32), primary_key=True,
                default=lambda: uuid.uuid4().hex)
    private_id = Column(String(32), index=True,
                        default=lambda: uuid.uuid4().hex)
    created = Column(TIMESTAMP(timezone=True), unique=True, nullable=False, index=True,
                     default=lambda: dt.datetime.now(dt.timezone.utc))
    title = Column(Unicode, nullable=True)
    description = Column(Unicode, nullable=True)

    @classmethod
    def fields(cls):
        """Exposes the definition of the draw as a dict

        For each field the following is returned:
            type: SQLAlchemy type
            optional: bool. Whether the field needs to be passed in or not
        """
        return {
            c.key: dict(
                type=c.type,
                optional=c.nullable or (c.default is not None),
            )
            for c in cls.__table__.columns
        }

    def __repr__(self):
        return f'<{self.__class__.__name__} {repr(self.id)}>'


class RandomNumber(DrawBaseModel, SQLFactory):
    __tablename__ = 'random_number'
    DEFAULT_MIN = 1
    DEFAULT_MAX = 10

    range_min = Column(Integer, nullable=False,
                       default=DEFAULT_MIN)
    range_max = Column(Integer, nullable=False,
                       default=DEFAULT_MAX)
    __table_args__ = (
        _positive_number("range_min"),
        _positive_number("range_max"),
        sqlalchemy.CheckConstraint(
            range_min < range_max,
            name="range_min_lt_range_max"
        ),
    )
