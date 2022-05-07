from flask import Flask, session, g
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import User


@app.before_request
def before_request():
    username = session.get('username')
    if username:
        user_ogj = User.query.filter(User.username == username).first()
        setattr(g, 'user', user_ogj)
    else:
        setattr(g, 'user', None)


@app.context_processor
def context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    else:
        return {}


from app import routes, models
