import re
from flask import Flask, jsonify, make_response, request, url_for, redirect
from sqlalchemy import and_, select, asc
from sqlalchemy.ext.automap import automap_base
from config import Config
from exts import db
# from models import MenRankingDb


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    men_ranking_db = db.Table("men_ranking", db.metadata, autoload_with=db.engine)


@app.route("/fifa-point-calculator/api/countryCodeList", methods=["GET"])
def get_country_codes():
    params = request.args
    periode = params.get("periode")
    date_pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")

    if len(params) == 1 and date_pattern.match(periode) and periode:
        select_stmt = select(men_ranking_db.c.country_code, men_ranking_db.c.name).where(men_ranking_db.c.periode.__eq__(periode)).order_by(asc(men_ranking_db.c.country_code))
        items = [item._asdict() for item in db.session.execute(select_stmt).all()]
    else:
        items = []

    response = make_response(jsonify(dataItems=items))
    response.status_code = 200
    return response


@app.route("/fifa-point-calculator/api/data", methods=["GET"])
def get_ranking():
    params = request.args
    country_code = params.get("countryCode")
    country_name = params.get("name")
    periode = params.get("periode")
    date_pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")
    
    if len(params) == 1 and country_code:
        select_stmt = select(men_ranking_db.c[1:]).where(men_ranking_db.c.country_code.__eq__(country_code.upper()))
        items = [item._asdict() for item in db.session.execute(select_stmt).all()]
    elif len(params) == 1 and country_name:
        select_stmt = select(men_ranking_db.c[1:]).where(men_ranking_db.c.name.like(f"%{country_name.title()}%"))
        items = [item._asdict() for item in db.session.execute(select_stmt).all()]
    elif len(params) == 1 and periode and date_pattern.match(periode):
        select_stmt = select(men_ranking_db.c[1:]).where(men_ranking_db.c.periode.__eq__(periode))
        items = [item._asdict() for item in db.session.execute(select_stmt).all()]
    elif len(params) == 2 and periode and country_code and date_pattern.match(periode):
        select_stmt = select(men_ranking_db.c[1:]).where(
                and_(
                        men_ranking_db.c.country_code.__eq__(country_code.upper()),
                        men_ranking_db.c.periode.__eq__(periode)
                )
        )
        items = [item._asdict() for item in db.session.execute(select_stmt).all()]
    elif len(params) == 2 and country_name and periode and date_pattern.match(periode):
        select_stmt = select(men_ranking_db.c[1:]).where(
                and_(
                        men_ranking_db.c.name.like(f"%{country_name.title()}%"),
                        men_ranking_db.c.periode.__eq__(periode)
                )
        )
        items = [item._asdict() for item in db.session.execute(select_stmt).all()]
    elif len(params) == 2 and country_name and country_code:
        select_stmt = select(men_ranking_db.c[1:]).where(
                and_(
                        men_ranking_db.c.country_code.__eq__(country_code.upper()),
                        men_ranking_db.c.name.like(f"%{country_name.title()}%")
                )
        )
        items = [item._asdict() for item in db.session.execute(select_stmt).all()]
    else:
        items = []
        
    response = make_response(jsonify(dataItems=items))
    response.status_code = 200
    return response


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()

    app.run(host="0.0.0.0", debug=True)
