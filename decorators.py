from http import HTTPStatus
from flask import request, make_response, jsonify
from marshmallow import ValidationError


def request_validator(schema):
    def decorator(f):
        def wrapper(*args, **kwargs):
            try:
                params = request.args.to_dict()
                request_schema = schema()
                request_schema.load(params)
            except ValidationError as err:
                return make_response(jsonify(message=f"{HTTPStatus.BAD_REQUEST} Bad Request!!!", **err.messages), HTTPStatus.BAD_REQUEST)
            return f(*args, **kwargs)
        return wrapper
    return decorator
