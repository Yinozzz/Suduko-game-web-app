from app import app, db
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import RegisterForm, LoginForm
from app.models import User


@app.route('/')
def index():
    return "Hello, world"


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm(request.form)
    username = form.username.data
    password = form.password.data
    if request.method == 'POST':
        if form.validate_on_submit() and User.query.filter(User.username == username).first() is None:
            new_user = User(username=username,password=password)
            db.session.add(new_user)
            db.session.commit()
            return "successful"
        else:
            return "fail"
    return render_template('register.html', form=form)


@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    user = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        user_object = User.query.filter(User.username==user).first()
        if user_object is None:
            flash('invalid username or data')
            return redirect(url_for('login'))
        if user_object.password != password:
            flash('Incorrect password. Please try again.')
            return redirect(url_for('login'))
        # flash('Login requested for user {}, remember_me={}'.format(
        #     form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign in', form=form)



