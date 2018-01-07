from flask import request, Blueprint, jsonify

from . import models, schemas

bp = Blueprint("api", __name__)


_SCHEMAS = {
    "random_number": schemas.RandomNumber,
}

_MODELS = {
    "random_number": models.RandomNumber,
}


@bp.route("/<string:draw_type>", methods=["POST"])
def post(draw_type):
    serializer = _SCHEMAS[draw_type]()
    model_class = _MODELS[draw_type]

    input_data, _ = serializer.load(request.json)
    obj = model_class.create(**input_data)
    output_data, _ = serializer.dump(obj)
    return jsonify(output_data)


@bp.route("/<string:draw_type>/<string:id_>", methods=["GET"])
def get(draw_type, id_):
    serializer = _SCHEMAS[draw_type]()
    model_class = _MODELS[draw_type]

    input_data, _ = serializer.load(request.json)
    obj = model_class.query.get(id_)
    output_data, _ = serializer.dump(obj)
    return jsonify(output_data)
