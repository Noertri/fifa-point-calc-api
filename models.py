from exts import db
from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, Float, Text


class MenRankingDb(db.Model):
    __tablename__ = "men_ranking"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    date = mapped_column(Text)
    country_code = mapped_column(Text)
    name = mapped_column(Text)
    rank = mapped_column(Integer)
    prev_rank = mapped_column(Integer)
    points = mapped_column(Float)
    prev_points = mapped_column(Float)
    zone = mapped_column(Text)

    def asdict(self):
        return {
            "countryCode": self.country_code,
            "name": self.name,
            "rank": self.rank,
            "previousRank": self.prev_rank,
            "points": self.points,
            "previousPoints": self.prev_points,
            "zone": self.zone
        }
