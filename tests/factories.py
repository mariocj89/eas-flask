from functools import partial

import factory as fb

from eas import models


Faker = partial(fb.Faker, locale="es_ES")


class BaseFactory(fb.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = models.db.session

    @classmethod
    def dict(cls, **kwargs):
        """Returns a dict rather than an object"""
        return fb.build(dict, FACTORY_CLASS=cls, **kwargs)


class ComplexDraw(BaseFactory):
    title = Faker("sentence")
    description = Faker("text")


class SimpleNumber(BaseFactory):
    class Meta:
        model = models.RandomNumber

    range_min = 1
    range_max = 10


class PublicNumber(ComplexDraw):
    class Meta:
        model = models.RandomNumber

    range_min = 5
    range_max = 22


class FacebookRaffle(ComplexDraw):
    class Meta:
        model = models.FacebookRaffle

    facebook_object_id = "87e97ew98r798ew7r98ew78"
    prices = fb.List(
        Faker("sentence") for _ in range(3)
    )
