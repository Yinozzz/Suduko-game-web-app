from app import app, db
from flask import render_template, request, flash, redirect, url_for
from app.forms import RegisterForm, LoginForm
from app.models import User


@app.route('/')
def index():
    return "Hello, world"


@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        new_user = User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
    return render_template('register.html', form=form)


@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)



