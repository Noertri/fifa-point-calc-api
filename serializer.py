from marshmallow import fields
from exts import ma


class RankingSchema(ma.Schema):
    currentPoints = fields.Float(attribute="current_points")
    prevPoints = fields.Float(attribute="prev_points")
    currentRank = fields.Integer(attribute="current_rank")
    prevRank = fields.Integer(attribute="prev_rank")
    periode = fields.String(attribute="periode")


class MenRankingSchema(ma.Schema):
    countryCode = fields.String(attribute="country_code")
    name = fields.String(attribute="country_name")
    zone = fields.String(attribute="country_zone")
    data = fields.Nested(RankingSchema, many=True, attribute="men_rank_data")


class RequestSchema(ma.Schema):
    pass
