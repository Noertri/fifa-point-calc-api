import re
from flask import Flask, jsonify, make_response, request
from config import Config
from exts import db, ma
import sqlalchemy as sa
from models import FIFACountryDb, MenRankingDb
from serializer import MenRankingSchema


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)


@app.route("/fifa-point-calculator/api/ranking", methods=["GET"])
def get_ranking():
    params = request.args.to_dict()
    country_code = params.get("countryCode")
    periode = params.get("periode")
    country_name = params.get("countryName")
    date_pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")

    if len(params) == 1 and periode and date_pattern.match(periode):
        select_stmt = sa.select(FIFACountryDb)
        join_stmt = select_stmt.join(MenRankingDb).where(MenRankingDb.periode == periode).order_by(sa.asc(MenRankingDb.current_rank))
        results = db.session.execute(join_stmt).scalars().all()
        country_schema = MenRankingSchema()
        items = country_schema.dump(results, many=True)
    elif len(params) == 2 and periode and date_pattern.match(periode) and country_name:
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
    elif len(params) == 2 and periode and date_pattern.match(periode) and country_code:
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
    else:
        items = []
        
    response = make_response(jsonify(items))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run()
