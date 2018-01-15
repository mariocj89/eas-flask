from marshmallow import fields, Schema, post_load, ValidationError

from . import models


def _positive(input_number):
    """Validator that checks a number is positive"""
    if input_number < 0:
        raise ValidationError("Number has to be positive")


class DrawResultSchema(Schema):
    created = fields.DateTime(dump_only=True)
    value = fields.Raw(dump_only=True)


class DrawBaseSchema(Schema):
    id = fields.Str(dump_only=True)
    private_id = fields.Str(dump_only=True)
    created = fields.DateTime(dump_only=True)
    title = fields.String()
    description = fields.String()
    results = fields.Nested(DrawResultSchema, many=True)


class RandomNumber(DrawBaseSchema):
    range_min = fields.Integer(validate=_positive, required=True)
    range_max = fields.Integer(validate=_positive, required=True)

    @post_load
    def _make(self, data):
        if not data["range_min"] < data["range_max"]:
            raise ValidationError(
                "range_min needs to be smaller than range_max",
                ["range_min"]
            )
        return models.RandomNumber(**data)
