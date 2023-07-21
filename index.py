from flask import Flask, request, make_response, jsonify
from exts import db
from models import MenRankingDb
from sqlalchemy import select, and_, or_
import os


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(os.getcwd(), "fifa_rankings.sqlite")
# app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)


@app.route("/api/ranking", methods=["GET"])
def get_ranking():
    if request.method == "GET":
        params = request.args
        country_code = params.get("countryCode", type=str)
        country_name = params.get("name", type=str)
        periode = params.get("periode", type=str)
        select_stmt = select(MenRankingDb)
        
        if len(params) == 1 and country_code:
            select_stmt.where(MenRankingDb.country_code.__eq__(country_code.upper()))
        elif len(params) == 1 and country_name:
            select_stmt.where(MenRankingDb.name.like(f"%{country_name.title()}%"))
        elif len(params) == 1 and periode:
            select_stmt.where(MenRankingDb.date.__eq__(periode))
            
        items = [item.asdict() for item in db.session.execute(select_stmt).scalars()]
        response = make_response(jsonify(rankingItems=items, lang="en"))
        response.status_code = 200
        return response


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
