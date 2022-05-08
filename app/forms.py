from flask_wtf import FlaskForm
import wtforms
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(wtforms.Form):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])


class LoginForm(wtforms.Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class GameTableForm(wtforms.Form):
    number_string = StringField('Number_string', validators=[DataRequired()])