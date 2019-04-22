from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
#local
from uifactory.models import Users


class RegistrationForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.get_user_by_user_name(username=email.data)
        if user:
            raise ValidationError('That email is already in use. Please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddPlantForm(FlaskForm):
    pl_name = StringField('Plant Name', validators=[DataRequired(), Length(min=3, max=50)])
    pl_type = StringField('Plant Type', validators=[DataRequired(), Length(min=3, max=50)])
    sen_id = StringField('Sensor Id', validators=[DataRequired(), Length(min=12, max=12)])
    submit = SubmitField('Add Plant')
