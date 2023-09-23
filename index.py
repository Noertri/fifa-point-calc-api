import re
from flask import Flask, jsonify, make_response, request
from sqlalchemy import and_, asc, select
from config import Config
from exts import db


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    men_ranking_db = db.Table("men_ranking", db.metadata, autoload_with=db.engine)


@app.route("/fifa-point-calculator/api/ranking", methods=["GET"])
def get_ranking():
    params = request.args
    country_code = params.get("countryCode")
    periode = params.get("periode")
    country_name = params.get("countryName")
    date_pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")
    
    if len(params) == 1 and periode and date_pattern.match(periode):
        select_stmt = select(men_ranking_db.c[1:]).where(men_ranking_db.c.periode.__eq__(periode)).order_by(asc(men_ranking_db.c.rank))
        items = [item._asdict() for item in db.session.execute(select_stmt).all()]
    elif len(params) == 2 and periode and country_code and date_pattern.match(periode):
        select_stmt = select(men_ranking_db.c[1:]).where(
                and_(
                        men_ranking_db.c.country_code.__eq__(country_code.upper()),
                        men_ranking_db.c.periode.__eq__(periode)
                )
        )
        items = [item._asdict() for item in db.session.execute(select_stmt).all()]
    elif len(params) == 2 and periode and country_name and date_pattern.match(periode):
        select_stmt = select(men_ranking_db.c[1:]).where(
                and_(
                        men_ranking_db.c.name.like(f"%{country_name.title()}%"),
                        men_ranking_db.c.periode.__eq__(periode)
                )
        )
        items = [item._asdict() for item in db.session.execute(select_stmt).all()]
    else:
        items = []
        
    response = make_response(jsonify(dataItems=items))
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5502)
