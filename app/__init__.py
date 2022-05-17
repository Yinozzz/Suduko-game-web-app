from flask import Flask, session, g
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import time
from datetime import date

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import User, GameBank


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


@app.before_first_request
def before_first_request():
    default1 = '6,9,5,1,2,3,7,4,8,7,4,1,8,6,9,2,5,3,2,3,8,4,5,7,1,6,9,8,1' \
               ',6,7,4,5,3,9,2,5,2,4,3,9,8,6,7,1,3,7,9,6,1,2,4,' \
               '8,5,4,8,3,9,7,1,5,2,6,1,6,2,5,8,4,9,3,7,9,5,7,2,3,6,8,1,4'
    default2 = '7,4,9,5,2,3,8,1,6,5,2,3,1,6,8,4,9,7,8,6,1,9,4,7,5,3,2,6,7,2,4,1,9,3,8,5,4,9,5,' \
               '8,3,6,7,2,1,1,3,8,2,7,5,9,6,4,3,8,6,7,5,2,1,4,9,9,5,4,6,8,1,2,7,3,2,1,7,3,9,4,6,5,8'
    if User.query.filter(User.username == 'admin').first() is None:
        admin = User(username='admin', password='123456', user_type=0, head_pic_url='./static/default_head_pic.jpg')
        db.session.add(admin)
        db.session.commit()
    if GameBank.query.filter(GameBank.game == default1).first() is None:
        default_game = GameBank(uploaderId=1, game=default1, upload_time=date.fromtimestamp(time.time()))
        db.session.add(default_game)
        db.session.commit()


from app import routes, models, api


