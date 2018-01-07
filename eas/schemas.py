from marshmallow import fields, Schema


class DrawBaseSchema(Schema):
    id = fields.Str(dump_only=True)
    created = fields.DateTime(dump_only=True)
    title = fields.String()
    description = fields.String()


class RandomNumber(DrawBaseSchema):
    range_min = fields.Integer()
    range_max = fields.Integer()
