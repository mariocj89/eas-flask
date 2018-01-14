import factory as fb

from eas import models


class _WithTitleAndDesc:
    title = "Example title"
    description = "Not so long description"


class BaseFactory(fb.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = models.db.session

    @classmethod
    def dict(cls, **kwargs):
        """Returns a dict rather than an object"""
        return fb.build(dict, FACTORY_CLASS=cls, **kwargs)


class SimpleNumber(BaseFactory):
    class Meta:
        model = models.RandomNumber

    range_min = 1
    range_max = 10


class PublicNumber(_WithTitleAndDesc, SimpleNumber):
    pass

