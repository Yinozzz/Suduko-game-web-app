from app import app
from flask import render_template
from app.forms import RegisterForm
from app.models import User


@app.route('/')
def index():
    return "Hello, world"


@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)
