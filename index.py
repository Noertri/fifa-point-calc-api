from http import HTTPStatus
import sqlalchemy as sa
from flask import Flask, jsonify, make_response, request
from config import Config
from decorators import request_validator
from exts import db, ma
from models import FIFACountryDb, MenRankingDb
from schemas import MenRankingSchema, RequestSchema

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)


@app.route("/fifa-point-calculator/api/ranking", methods=["GET"])
@request_validator(RequestSchema)
def get_ranking():
    params = request.args.to_dict()
    country_code = params.get("countryCode")
    periode = params.get("periode")
    country_name = params.get("countryName")
    country_zone = params.get("zone")

    if len(params) == 1 and periode:
        select_stmt = sa.select(FIFACountryDb)
        join_stmt = select_stmt.join(MenRankingDb).where(MenRankingDb.periode == periode).order_by(sa.asc(MenRankingDb.current_rank))
        results = db.session.execute(join_stmt).scalars().all()
        country_schema = MenRankingSchema()
        items = country_schema.dump(results, many=True)
    elif len(params) == 2 and periode and country_name:
        select_stmt = sa.select(FIFACountryDb)
        join_stmt = select_stmt.join(MenRankingDb).where(
                sa.and_(
                        MenRankingDb.periode == periode,
                        FIFACountryDb.country_name.like(f"%{country_name.lower()}%")
                )
        ).order_by(sa.asc(MenRankingDb.current_rank))
        results = db.session.execute(join_stmt).scalars().all()
        country_schema = MenRankingSchema()
        items = country_schema.dump(results, many=True)
    elif len(params) == 2 and periode and country_code:
        select_stmt = sa.select(FIFACountryDb)
        join_stmt = select_stmt.join(MenRankingDb).where(
                sa.and_(
                        MenRankingDb.periode == periode,
                        FIFACountryDb.country_code.like(f"%{country_code.lower()}%")
                )
        ).order_by(sa.asc(MenRankingDb.current_rank))
        results = db.session.execute(join_stmt).scalars().all()
        country_schema = MenRankingSchema()
        items = country_schema.dump(results, many=True)
    elif len(params) == 2 and periode and country_zone:
        select_stmt = sa.select(FIFACountryDb)
        join_stmt = select_stmt.join(MenRankingDb).where(
                sa.and_(
                        MenRankingDb.periode == periode,
                        FIFACountryDb.country_zone == country_zone.upper()
                )
        ).order_by(sa.asc(MenRankingDb.current_rank))
        results = db.session.execute(join_stmt).scalars().all()
        country_schema = MenRankingSchema()
        items = country_schema.dump(results, many=True)
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
