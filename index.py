from http import HTTPStatus
import sqlalchemy as sa
from flask import Flask, jsonify, make_response, request
from config import Config
from decorators import request_validator
from exts import db, ma
from models import FIFACountryDb, MenRankingDb
from schemas import RankingSchema, RequestSchema

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)


@app.route("/fifa-point-calculator/api/ranking/men", methods=["GET"])
@request_validator(RequestSchema)
def get_ranking():
    params = request.args.to_dict()
    periode = params.get("periode")

    if len(params) == 1 and periode:
        select_stmt = sa.select(
            FIFACountryDb.country_code,
            FIFACountryDb.country_name,
            FIFACountryDb.country_zone,
            MenRankingDb.periode,
            MenRankingDb.current_points,
            MenRankingDb.prev_points,
            MenRankingDb.current_rank,
            MenRankingDb.prev_rank
        ).select_from(FIFACountryDb)
        join_stmt = select_stmt.join(MenRankingDb, FIFACountryDb.country_code == MenRankingDb.country_code).where(MenRankingDb.periode == periode).order_by(sa.asc(MenRankingDb.current_rank))
        results = [r._asdict() for r in db.session.execute(join_stmt).all()]
        
        none_ranks = []
        for i, data in enumerate(results):
            if data.get("current_rank") is None:
                pop_item = results.pop(i)
                none_ranks.insert(-1, pop_item)

        results.extend(none_ranks)

        ranking_schema = RankingSchema()
        items = ranking_schema.load(results, many=True)
    else:
        items = []
        
    if items:
        response = make_response(jsonify(items), HTTPStatus.OK)
    else:
        response = make_response(jsonify(items), HTTPStatus.NOT_FOUND)
        
    response.headers.add("Access-Control-Allow-Origin", "*")
        
    return response


if __name__ == "__main__":
    app.run(port=5506)
