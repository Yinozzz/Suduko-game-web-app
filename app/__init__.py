from flask import Flask, session, g

from config import Config, Test_Config_Unit, Test_Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import time
from datetime import date
from werkzeug.security import generate_password_hash

app = Flask(__name__)
# app.config.from_object(Config)
# app.config.from_object(Test_Config)
app.config.from_object(Test_Config_Unit)
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
    default3 = '2,1,9,5,3,6,8,4,7,8,7,3,1,4,2,9,6,5,6,5,4,9,8,7,1,3,' \
               '2,4,9,8,7,5,3,2,1,6,1,6,7,4,2,9,3,5,8,3,2,5,8,6,1,7,9,4,' \
               '5,4,1,2,9,8,6,7,3,7,8,6,3,1,5,4,2,9,9,3,2,6,7,4,5,8,1'
    default4 = '9,8,7,6,5,1,4,3,2,6,5,3,4,2,8,7,1,9,4,2,1,3,9,7,6,8,5,7,9,5,' \
               '1,4,6,8,2,3,8,4,2,5,7,3,9,6,1,3,1,6,2,8,9,5,4,7,2,6,9,7,1,4,' \
               '3,5,8,1,3,8,9,6,5,2,7,4,5,7,4,8,3,2,1,9,6'
    # upload test "8,1,7,6,5,9,4,2,3,6,5,3,4,2,8,7,1,9,4,2,9,3,1,7,6,8,5,7,8,2,5,4,6,9,3,1,,3,6,5,7,9,1,8,4,2,9,4,1,2,8,3,5,6,7,2,9,6,1,7,4,3,5,8,1,3,8,9,6,5,2,7,4,5,7,4,8,3,2,1,9,6"
    if User.query.filter(User.username == 'admin').first() is None:
        admin = User(username='admin', password=generate_password_hash('123456'), user_type=0, head_pic_url='./static/default_head_pic.jpg')
        db.session.add(admin)
        db.session.commit()
    default_list = list()
    default_list.append(default1)
    default_list.append(default2)
    default_list.append(default3)
    default_list.append(default4)
    for index in range(len(default_list)):
        if GameBank.query.filter(GameBank.game == default_list[index]).first() is None:
            if index == 0:
                default_game = GameBank(uploaderId=1, game=default_list[index],
                                        upload_time=date.fromtimestamp(time.time()),
                                        current_game=time.strftime("%Y%m%d", time.localtime()))
            else:
                default_game = GameBank(uploaderId=1, game=default_list[index],
                                        upload_time=date.fromtimestamp(time.time()),
                                        current_game='')
            db.session.add(default_game)
            db.session.commit()


from app import routes, models


