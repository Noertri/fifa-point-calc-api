from marshmallow import fields, validate
from exts import ma
import re


class RankingSchema(ma.Schema):
    countryCode = fields.String(data_key="country_code")
    name = fields.String(data_key="country_name")
    zone = fields.String(data_key="country_zone")
    currentPoints = fields.Float(data_key="current_points", allow_nan=True, allow_none=True)
    previousPoints = fields.Float(data_key="prev_points", allow_nan=True, allow_none=True)
    currentRank = fields.Integer(data_key="current_rank", allow_none=True, strict=True)
    previousRank = fields.Integer(data_key="prev_rank", allow_none=True, strict=True)
    periode = fields.String(data_key="periode")


class RequestSchema(ma.Schema):
    periode = fields.String(required=True, validate=validate.Regexp(re.compile(r"\d{4}-\d{2}-\d{2}"), error="String does not match expected pattern. Expected pattern is yyyy-mm-dd!!!"))
