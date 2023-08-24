import os


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(os.getcwd(), "fifa_rankings.sqlite")
