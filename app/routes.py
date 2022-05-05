from app import app
from app.forms import LoginForm
from flask import render_template, flash, redirect, url_for
from app.forms import RegisterForm
from app.models import User


@app.route('/')
def index():
    return "Hello, world"


@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)



