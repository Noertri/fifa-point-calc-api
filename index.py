from flask import Flask, request, make_response, jsonify
from exts import db
from models import MenRankingDb
from sqlalchemy import select, and_


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fifa_rankings.sqlite"
db.init_app(app)


@app.route("/api/ranking", methods=["GET"])
def get_ranking():
    if request.method == "GET":
        params = request.args
        if 0 < len(params) <= 2:
            if country_code := params.get("countryCode", type=str):
                select_stmt = select(MenRankingDb).where(MenRankingDb.country_code == country_code.upper())
                items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
                response = make_response(jsonify(rankingItems=items, lang="en"))
                response.status_code = 200
                return response
            elif country_name := params.get("name", type=str):
                select_stmt = select(MenRankingDb).where(MenRankingDb.name.like(f"%{country_name.title()}%"))
                items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
                response = make_response(jsonify(rankingItems=items, lang="en"))
                response.status_code = 200
                return response
            elif periode := params.get("periode", type=str):
                select_stmt = select(MenRankingDb).where(MenRankingDb.date.__eq__(periode))
                items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
                response = make_response(jsonify(rankingItems=items, lang="en"))
                response.status_code = 200
                return response
            elif (country_name := params.get("name", type=str)) and (periode := params.get("periode", type=str)):
                select_stmt = select(MenRankingDb).where(and_(
                    MenRankingDb.name.like(f"%{country_name.title()}%"),
                    MenRankingDb.date.__eq__(periode)
                ))
                items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
                response = make_response(jsonify(rankingItems=items, lang="en"))
                response.status_code = 200
                return response
            elif (country_code := params.get("countryCode", type=str)) and (periode := params.get("periode", type=str)):
                select_stmt = select(MenRankingDb).where(and_(
                    MenRankingDb.country_code.__eq__(country_code.upper()),
                    MenRankingDb.date.__eq__(periode)
                ))
                items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
                response = make_response(jsonify(rankingItems=items, lang="en"))
                response.status_code = 200
                return response
        else:
            select_stmt = select(MenRankingDb)
            items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
            response = make_response(jsonify(rankingItems=items, lang="en"))
            response.status_code = 200
            return response


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
