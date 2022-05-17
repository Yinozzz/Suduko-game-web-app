import os
import time

from sqlalchemy import func

from app import app, db
from flask import render_template, request, flash, redirect, url_for, session, g
from app.forms import RegisterForm, LoginForm, GameTableForm
from app.models import User, GameResult, GameBank
from werkzeug.security import generate_password_hash, check_password_hash
import json
import random


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/introduction')
def introduction():
    return render_template('introduction.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        username = form.username.data
        password = generate_password_hash(form.password.data)
        if form.validate():
            if User.query.filter(User.username == username).first() is None:
                new_user = User(username=username, password=password, user_type=1)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                flash(" The user name already exists. ")
                return redirect(url_for('register'))
        else:
            flash(" Incorrect user name or password format. ")
            return redirect(url_for('register'))


@app.route('/login', methods=['GET', 'POST'])
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
            elif not check_password_hash(user_object.password, password):
                flash('Incorrect password. Please try again.')
                return redirect(url_for('login'))
            else:
                if request.form.get('remember') == '1':
                    session.permanent = True
                session['username'] = username
                return redirect(url_for('game'))
        else:
            flash('not empty.')
            return redirect(url_for('login'))


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == "GET":
        game_bank_obj = GameBank.query.filter(GameBank.id == 1).first()
        # random.seed(g.user.id)
        if g.user:
            random.seed(g.user.id)
            user_flag = g.user
            is_admin = User.query.filter(User.id == g.user.id).first().user_type
        else:
            random.seed(1)
            user_flag = None
            is_admin=1
        random_list = random.sample(range(0, 81), 43)

        player_best_ranks = db.session.query(GameResult.playerId,
                                             func.min(GameResult.time_spent)).group_by(GameResult.playerId).order_by(
            GameResult.time_spent).all()
        print(player_best_ranks)
        rank_list = list()
        for i in range(len(player_best_ranks)):
            temp_dict = dict()
            temp_dict["player_name"] = User.query.filter(User.id == player_best_ranks[i][0]).first().username
            temp_dict["best_mark"] = player_best_ranks[i][1]
            temp_dict["rank"] = i + 1
            rank_list.append(temp_dict)
        # rank_json = json.dumps(rank_dict)
        return render_template('game.html', game=game_bank_obj.game.split(','), random_list=random_list,
                               user_flag=user_flag, rank_list=rank_list, is_admin=is_admin)
    else:
        rows = True
        columns = True
        grids = True
        data_string = request.get_json()
        print(data_string)
        listdata = data_string['game_string'].split(',')
        final_list = list()
        for i in range(0, len(listdata), 9):
            final_list.append(listdata[i:i + 9])

        for i in range(len(final_list)):
            temp_col = list()
            for j in range(len(final_list)):
                temp_col.append(final_list[j][i])
            if len(final_list[i]) != len(set(final_list[i])):
                rows = False
            if len(temp_col) != len(set(temp_col)):
                columns = False
        for i in [1, 4, 7]:
            for j in [1, 4, 7]:
                temp_grid = list()
                temp_grid.append(final_list[i - 1][j - 1])
                temp_grid.append(final_list[i - 1][j])
                temp_grid.append(final_list[i - 1][j + 1])
                temp_grid.append(final_list[i][j - 1])
                temp_grid.append(final_list[i][j])
                temp_grid.append(final_list[i][j + 1])
                temp_grid.append(final_list[i + 1][j - 1])
                temp_grid.append(final_list[i + 1][j])
                temp_grid.append(final_list[i + 1][j + 1])
                if len(temp_grid) != len(set(temp_grid)):
                    grids = False
        if rows and columns and grids:
            input_db_data = GameResult(playerId=g.user.id,
                                       start_time=data_string['start_time'],
                                       finish_time=data_string['finish_time'],
                                       time_spent=(data_string['finish_time'] - data_string['start_time']))
            db.session.add(input_db_data)
            db.session.commit()
            return "success"
        else:
            return "fail"


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


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "GET":
        # game_bank_obj = GameBank.query.filter(GameBank.id == 1).first()
        # # random.seed(g.user.id)
        # random.seed(1)
        # random_list = random.sample(range(0, 81), 43)
        # print(random_list)
        return render_template('upload.html')
    else:
        rows = True
        columns = True
        grids = True
        data_string = request.get_json()
        listdata = data_string['game_string'].split(',')
        final_list = list()
        for i in range(0, len(listdata), 9):
            final_list.append(listdata[i:i + 9])

        for i in range(len(final_list)):
            temp_col = list()
            for j in range(len(final_list)):
                temp_col.append(final_list[j][i])
            if len(final_list[i]) != len(set(final_list[i])):
                rows = False
            if len(temp_col) != len(set(temp_col)):
                columns = False
        for i in [1, 4, 7]:
            for j in [1, 4, 7]:
                temp_grid = list()
                temp_grid.append(final_list[i - 1][j - 1])
                temp_grid.append(final_list[i - 1][j])
                temp_grid.append(final_list[i - 1][j + 1])
                temp_grid.append(final_list[i][j - 1])
                temp_grid.append(final_list[i][j])
                temp_grid.append(final_list[i][j + 1])
                temp_grid.append(final_list[i + 1][j - 1])
                temp_grid.append(final_list[i + 1][j])
                temp_grid.append(final_list[i + 1][j + 1])
                if len(temp_grid) != len(set(temp_grid)):
                    grids = False
        if rows and columns and grids:
            input_db_data = GameBank(game=data_string['game_string'],
                                     uploaderId=g.user.id,
                                     upload_time=None)
            db.session.add(input_db_data)
            db.session.commit()
            return "success"
        else:
            return "fail"


@app.route('/personal', methods=['GET', 'POST'])
def personal():
    # current_user = request.args.get('id', 0)
    result_dict = dict()
    if g.user:
        user_id = g.user.id
        user_query_set = User.query.filter(User.id == user_id).first()
        rank_query_set = GameResult.query.filter(GameResult.playerId == user_id)
        result_dict['username'] = user_query_set.username
        result_dict['head_pic_url'] = user_query_set.head_pic_url
        result_dict['rank_list'] = list()
        for one_game in rank_query_set:
            one_rank_dict = dict()
            one_rank_dict['time_spent'] = one_game.time_spent
            result_dict['rank_list'].append(one_rank_dict)
        return render_template('personal.html', result_dict=result_dict)
    else:
        return redirect(url_for('login'))


@app.route('/avatar', methods=['POST'])
def avatar_upload():
    temp_pic = request.files.get('headpic')
    if g.user:

        # temp_pic_path = os.path.join('./app/static/avatar'+random_name+'.jpg')
        temp_pic_path = User.query.filter(User.id == g.user.id).first().head_pic_url
        temp_pic_path = temp_pic_path.replace('./', './app/')
        print(temp_pic_path)
        front_end_url = './static/avatar'+str(g.user.id)+time.strftime("%Y%m%d%H%M%S", time.localtime()) +'.jpg'
        create_url = front_end_url.replace('./', './app/')
        if os.path.exists(temp_pic_path):
            os.remove(temp_pic_path)
        temp_pic.save(create_url)
        user_info = User.query.filter(User.id == g.user.id).first()
        if not user_info:
            return redirect(url_for('register'))
        else:
            user_info.head_pic_url = front_end_url
            db.session.merge(user_info)
            db.session.commit()
        return front_end_url
    else:
        return redirect(url_for('login'))


