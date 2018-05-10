"""Defintion of the endpoints for EAS api"""
from flask import request, Blueprint, jsonify

from . import models, schemas, swagger

bp = Blueprint("api", __name__)


_SCHEMAS = {
    "random_number": schemas.RandomNumber,
}

_MODELS = {
    "random_number": models.RandomNumber,
}


@bp.route("/swagger.yaml")
def serve_swagger_file():
    """Serves the swagger yaml definition"""
    return swagger.YAML_DEFINITION, 200, {'Content-Type': 'text'}


@bp.route("/ping")
def server_ping():
    """Heath check endpoint"""
    return "pong", 200, {'Content-Type': 'text'}


@bp.errorhandler(schemas.ValidationError)
def handle_invalid_usage(error):
    """Transforms ValidationErrors into 400 HTTP responses"""
    response = jsonify(error.messages)
    response.status_code = 400
    return response


@bp.route("/<string:draw_type>", methods=["POST"])
def create_draw(draw_type):
    """Draw creation"""
    serializer = _SCHEMAS[draw_type](strict=True)

    obj, _ = serializer.load(request.get_json(force=True))
    models.db.session.add(obj)
    models.db.session.commit()

    output_data, _ = serializer.dump(obj)
    output_data["private_id"] = obj.private_id
    return jsonify(output_data)


@bp.route("/<string:draw_type>/<string:id_>", methods=["PUT"])
def toss_draw(draw_type, id_):
    """Toss of a draw"""
    model_class = _MODELS[draw_type]

    obj = model_class.get_draw_or_404(id_)
    obj.toss()
    models.db.session.add(obj)
    models.db.session.commit()

    return retrieve_draw_by_id(draw_type, id_)


@bp.route("/<string:draw_type>/<string:id_>", methods=["GET"])
def retrieve_draw_by_id(draw_type, id_):
    """Retrieves a draw via its public/private id"""
    serializer = _SCHEMAS[draw_type](exclude=["private_id"])
    model_class = _MODELS[draw_type]

    obj = model_class.get_draw_or_404(id_)
    output_data, _ = serializer.dump(obj)
    return jsonify(output_data)
