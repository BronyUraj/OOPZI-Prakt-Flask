from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_json import FlaskJSON
from flask_crontab import Crontab
from flask_caching import Cache


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
json = FlaskJSON(app)
crontab = Crontab(app)
cache = Cache(app)

from app import routes, models, cron
