from marshmallow import fields, validate, post_load
from exts import ma
import re


class RankingSchema(ma.Schema):
    country_code = fields.String()
    country_name = fields.String()
    country_zone = fields.String()
    current_points = fields.Float(allow_nan=True, allow_none=True)
    prev_points = fields.Float(allow_nan=True, allow_none=True)
    current_rank = fields.Integer(allow_none=True)
    prev_rank = fields.Integer(allow_none=True)
    periode = fields.String()

    @post_load
    def make_nested_dict(self, data, **kwargs):
        return {
            "countryName": data.get("country_name"),
            "countryCode": data.get("country_code"),
            "countryZone": data.get("country_zone"),
            "data": {
                "periode": data.get("periode"),
                "currentPoints": data.get("current_points"),
                "previousPoints": data.get("prev_points"),
                "currentRank": data.get("current_rank"),
                "previousRank": data.get("prev_rank")
            }
        }


class RequestSchema(ma.Schema):
    periode = fields.String(required=True, validate=validate.Regexp(re.compile(r"\d{4}-\d{2}-\d{2}"), error="String does not match expected pattern. Expected pattern is yyyy-mm-dd!!!"))
