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


@bp.route("/<string:draw_type>/", methods=["POST"])
def post(draw_type):
    serializer = _SCHEMAS[draw_type](strict=True)

    obj, _ = serializer.load(request.json)
    obj.toss()
    models.db.session.add(obj)
    models.db.session.commit()

    output_data, _ = serializer.dump(obj)
    output_data["private_id"] = obj.private_id
    return jsonify(output_data)


@bp.route("/<string:draw_type>/<string:id_>/", methods=["GET"])
def get(draw_type, id_):
    serializer = _SCHEMAS[draw_type](exclude=["private_id"])
    model_class = _MODELS[draw_type]

    obj = model_class.query.get(id_)
    if not obj:  # Not found, try to search via private_id
        obj = model_class.query.filter_by(private_id=id_).first_or_404()
    output_data, _ = serializer.dump(obj)
    return jsonify(output_data)

