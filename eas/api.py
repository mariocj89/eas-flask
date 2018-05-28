"""Defintion of the endpoints for EAS api"""
from flask import request, Blueprint, jsonify, views

from . import models, schemas, swagger

bp = Blueprint("api", __name__)


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


class BaseDrawView(views.MethodView):
    NAME = None
    SERIALIZER = None
    MODEL_CLASS = None

    def create_draw(self, data):
        """Creates a new draw"""
        serializer = self.SERIALIZER(strict=True)
        obj, _ = serializer.load(data)
        models.db.session.add(obj)
        models.db.session.commit()

        output_data, _ = serializer.dump(obj)
        output_data["private_id"] = obj.private_id
        return output_data

    def toss_draw(self, id_):
        """Generates a new result of a draw"""
        obj = self.MODEL_CLASS.query.filter_by(private_id=id_).first_or_404()
        obj.toss()
        models.db.session.add(obj)
        models.db.session.commit()

    def retrieve_draw(self, id_):
        """Retrieves a draw via its public/private id"""
        serializer = self.SERIALIZER(exclude=["private_id"])

        obj = self.MODEL_CLASS.get_draw_or_404(id_)
        output_data, _ = serializer.dump(obj)
        return output_data

    @classmethod
    def register_urls(cls, bp_):
        """Registers the view using its name in a blueprint"""
        bp_.add_url_rule(f"/{cls.NAME}",
                         view_func=cls.as_view(cls.NAME),
                         methods=["POST"])
        bp_.add_url_rule(f"/{cls.NAME}/<string:id_>",
                         view_func=cls.as_view(cls.NAME + "_item"),
                         methods=["GET", "PUT"])

    def post(self):
        output = self.create_draw(request.get_json(force=True))
        return jsonify(output)

    def put(self, id_):
        self.toss_draw(id_)
        return self.get(id_)

    def get(self, id_):
        return jsonify(self.retrieve_draw(id_))


class RandomNumber(BaseDrawView):
    NAME = "random_number"
    SERIALIZER = schemas.RandomNumber
    MODEL_CLASS = models.RandomNumber


class FacebookRaffle(BaseDrawView):
    NAME = "facebook_raffle"
    SERIALIZER = schemas.FacebookRaffle
    MODEL_CLASS = models.FacebookRaffle


RandomNumber.register_urls(bp)
FacebookRaffle.register_urls(bp)
