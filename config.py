import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    API_KEY = "6797106fd85191ea7335559677948c72" or os.environ.get("API_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False