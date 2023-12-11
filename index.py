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
    country_code = params.get("countryCode")
    periode = params.get("periode")
    country_name = params.get("countryName")
    country_zone = params.get("zone")

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
        join_stmt = select_stmt.join(MenRankingDb).where(sa.and_(MenRankingDb.periode == periode, 
                    FIFACountryDb.country_code == MenRankingDb.country_code)).order_by(sa.asc(MenRankingDb.country_code))
        results = [row._asdict() for row in db.session.execute(join_stmt).all()]
        ranking_schema = RankingSchema()
        items = ranking_schema.load(results, many=True)
    elif len(params) == 2 and periode and country_name:
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
        join_stmt = select_stmt.join(MenRankingDb).where(
                sa.and_(
                        MenRankingDb.periode == periode,
                        FIFACountryDb.country_name.like(f"%{country_name.lower()}%")
                )
        ).order_by(sa.asc(MenRankingDb.current_rank))
        results = [row._asdict() for row in db.session.execute(join_stmt).all()]
        ranking_schema = RankingSchema()
        items = ranking_schema.load(results, many=True)
    elif len(params) == 2 and periode and country_code:
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
        join_stmt = select_stmt.join(MenRankingDb).where(
                sa.and_(
                        MenRankingDb.periode == periode,
                        FIFACountryDb.country_code.like(f"%{country_code.lower()}%")
                )
        ).order_by(sa.asc(MenRankingDb.current_rank))
        results = [row._asdict() for row in db.session.execute(join_stmt).all()]
        ranking_schema = RankingSchema()
        items = ranking_schema.load(results, many=True)
    elif len(params) == 2 and periode and country_zone:
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
        join_stmt = select_stmt.join(MenRankingDb).where(
                sa.and_(
                        MenRankingDb.periode == periode,
                        FIFACountryDb.country_zone == country_zone.upper()
                )
        ).order_by(sa.asc(MenRankingDb.current_rank))
        results = [row._asdict() for row in db.session.execute(join_stmt).all()]
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
    app.run()
