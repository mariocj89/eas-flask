from flask import request, Blueprint, jsonify, g

from . import models, schemas

bp = Blueprint("api", __name__)


_SCHEMAS = {
    "random_number": schemas.RandomNumber,
}

_MODELS = {
    "random_number": models.RandomNumber,
}


@bp.errorhandler(schemas.ValidationError)
def handle_invalid_usage(error):
    response = jsonify(error.messages)
    response.status_code = 400
    return response


@bp.route("/<string:draw_type>", methods=["POST"])
def post(draw_type):
    serializer = _SCHEMAS[draw_type](strict=True)

    obj, _ = serializer.load(request.get_json(force=True))
    models.db.session.add(obj)
    models.db.session.commit()

    output_data, _ = serializer.dump(obj)
    output_data["private_id"] = obj.private_id
    return jsonify(output_data)


@bp.route("/<string:draw_type>/<string:id_>", methods=["PUT"])
def put(draw_type, id_):
    serializer = _SCHEMAS[draw_type](exclude=["private_id"])
    model_class = _MODELS[draw_type]

    obj = model_class.get_draw_or_404(id_)
    obj.toss()
    models.db.session.add(obj)
    models.db.session.commit()

    output_data, _ = serializer.dump(obj)
    return jsonify(output_data)


@bp.route("/<string:draw_type>/<string:id_>", methods=["GET"])
def get(draw_type, id_):
    serializer = _SCHEMAS[draw_type](exclude=["private_id"])
    model_class = _MODELS[draw_type]

    obj = model_class.get_draw_or_404(id_)
    output_data, _ = serializer.dump(obj)
    return jsonify(output_data)

