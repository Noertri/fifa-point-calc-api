from exts import db
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, Float, Text, ForeignKey, UniqueConstraint


class FIFACountryDb(db.Model):
    __tablename__ = "fifa_country"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_code = mapped_column(Text)
    country_name = mapped_column(Text)
    country_zone = mapped_column(Text)
    rank_data = relationship("MenRankingDb", back_populates="country")
    UniqueConstraint(country_code, country_name)
    

class MenRankingDb(db.Model):
    __tablename__ = "men_ranking"
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    periode = mapped_column(Text)
    country_code = mapped_column(Text, ForeignKey("fifa_country.country_code"))
    current_rank = mapped_column(Integer)
    prev_rank = mapped_column(Integer)
    current_points = mapped_column(Float)
    prev_points = mapped_column(Float)
    country = relationship("FIFACountryDb", back_populates="rank_data")
