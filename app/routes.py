from sqlalchemy import func

from app import app, db
from flask import render_template, request, flash, redirect, url_for, session, g
from app.forms import RegisterForm, LoginForm, GameTableForm
from app.models import User, GameResult
import json

@app.route('/')
def index():
    return "Hello, world"


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        username = form.username.data
        password = form.password.data
        if form.validate() and User.query.filter(User.username == username).first() is None:
            new_user = User(username=username,password=password)
            db.session.add(new_user)
            db.session.commit()
            return "successful"
        else:
            return "fail"


@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        username = form.username.data
        password = form.password.data
        if form.validate():
            user_object = User.query.filter(User.username == username).first()
            if user_object is None:
                flash('invalid username or data')
                return redirect(url_for('login'))
            elif user_object.password != password:
                flash('Incorrect password. Please try again.')
                return redirect(url_for('login'))
            else:
                session['username'] = username
                return redirect(url_for('game'))
        else:
            flash('not empty.')
            return redirect(url_for('login'))


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == "GET":
        return render_template('game.html')
    else:
        form = GameTableForm(request.form)
        data_string = form.number_string.data
        data_string = data_string.replace('\n', '')
        return data_string


@app.route('/rank', methods=['GET', 'POST'])
def rank():
    if request.method == "GET":
        player_best_ranks = db.session.query(GameResult.playerId,
                                             func.min(GameResult.time_spent)).group_by(GameResult.playerId).all()
        print(player_best_ranks)
        rank_dict = dict()
        for i in range(len(player_best_ranks)):
            temp_dict = dict()
            temp_dict["player_name"] = User.query.filter(User.id == player_best_ranks[i][0]).first().username
            temp_dict["best_mark"] = player_best_ranks[i][1]
            rank_dict[i] = temp_dict
        rank_json = json.dumps(rank_dict)
        return rank_json
    else:
        playerId = request.form.get('playerId')
        time_spent = request.form.get('time_spent')
        rank = GameResult(playerId=playerId, time_spent=time_spent)
        db.session.add(rank)
        db.session.commit()
        return ''



