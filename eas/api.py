from flask import request, Blueprint, jsonify

from . import models, schemas

blueprint = Blueprint("api", __name__)


def resource_create(model_class, serializer):
    input_data, _ = serializer.load(request.json)
    obj = model_class.create(**input_data)
    output_data, _ = serializer.dump(obj)
    return jsonify(output_data)


@blueprint.route("/random_number")
def post():
    return resource_create(models.RandomNumber, schemas.RandomNumber())
