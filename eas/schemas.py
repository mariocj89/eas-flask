"""Marshmallow schemas used across the APP"""
from marshmallow import fields, Schema, post_load, ValidationError

from . import models


def _positive(input_number):
    """Validator that checks a number is positive"""
    if input_number < 0:
        raise ValidationError("Number has to be positive")


class DrawResultSchema(Schema):
    """Schema of the result of a draw

    Contains the date it was created and a JSON with the result.
    The shape of the json depends on the draw.
    """
    created = fields.DateTime(dump_only=True)
    value = fields.Raw(dump_only=True)


class DrawBaseSchema(Schema):
    """Base schema for all draws"""
    id = fields.Str(dump_only=True)
    private_id = fields.Str(dump_only=True)
    created = fields.DateTime(dump_only=True)
    title = fields.String()
    description = fields.String()
    results = fields.Nested(DrawResultSchema, many=True)


class RandomNumber(DrawBaseSchema):
    """Schema for a RandomNumber draw"""
    range_min = fields.Integer(validate=_positive, required=True)
    range_max = fields.Integer(validate=_positive, required=True)

    @post_load
    def _make(self, data):  # pylint: disable=no-self-use
        if not data["range_min"] < data["range_max"]:
            raise ValidationError(
                "range_min needs to be smaller than range_max",
                ["range_min"]
            )
        return models.RandomNumber(**data)


class FacebookRaffle(DrawBaseSchema):
    """Schema for a FacebookRaffle Draw"""
    facebook_object_id = fields.Str(required=True)
    prices = fields.List(fields.String(), required=True)

    @post_load
    def _make(self, data):  # pylint: disable=no-self-use
        prices = data.pop("prices")
        if not len(prices):
            raise ValidationError(
                "Raffles should have a least one price",
                ["prices"]
            )
        raffle = models.FacebookRaffle(**data)
        map(raffle.add_price, prices)
        return raffle
