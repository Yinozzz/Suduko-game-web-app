from app import app, db
from flask import render_template, request, flash, redirect, url_for, session, g
from app.forms import RegisterForm, LoginForm
from app.models import User


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
    return render_template('game.html')



