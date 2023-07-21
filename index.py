import re
from flask import Flask, jsonify, make_response, request, url_for, redirect
from sqlalchemy import and_, select
from config import Config
from exts import db
from models import MenRankingDb


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route("/", methods=["GET"])
def home():
    return redirect(url_for("get_ranking"))


@app.route("/api/ranking", methods=["GET"])
def get_ranking():
    if request.method == "GET":
        params = request.args
        country_code = params.get("countryCode")
        country_name = params.get("name")
        periode = params.get("periode")
        date_pattern = re.compile(r"\d\d\d\d-\d\d-\d\d")
        
        if len(params) == 1 and country_code:
            select_stmt = select(MenRankingDb).where(MenRankingDb.country_code.__eq__(country_code.upper()))
            items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
        elif len(params) == 1 and country_name:
            select_stmt = select(MenRankingDb).where(MenRankingDb.name.like(f"%{country_name.title()}%"))
            items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
        elif len(params) == 1 and periode and date_pattern.match(periode):
            select_stmt = select(MenRankingDb).where(MenRankingDb.date.__eq__(periode))
            items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
        elif len(params) == 2 and periode and country_code and date_pattern.match(periode):
            select_stmt = select(MenRankingDb).where(
                    and_(
                            MenRankingDb.country_code.__eq__(country_code.upper()),
                            MenRankingDb.date.__eq__(periode)
                    )
            )
            items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
        elif len(params) == 2 and country_name and periode and date_pattern.match(periode):
            select_stmt = select(MenRankingDb).where(
                    and_(
                            MenRankingDb.name.like(f"%{country_name.title()}%"),
                            MenRankingDb.date.__eq__(periode)
                    )
            )
            items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
        elif len(params) == 2 and country_name and country_code:
            select_stmt = select(MenRankingDb).where(
                    and_(
                            MenRankingDb.country_code.__eq__(country_code.upper()),
                            MenRankingDb.name.like(f"%{country_name.title()}%")
                    )
            )
            items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
        elif len(params) == 0:
            select_stmt = select(MenRankingDb)
            items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
        else:
            items = []
            
        response = make_response(jsonify(rankingItems=items, lang="en"))
        response.status_code = 200
        return response


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0")
