from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField,PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from reportit import session
from reportit.models import User


class RegistrationForm(FlaskForm):
    fname = StringField('First Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    nationalid = StringField('National ID',
                        validators=[DataRequired(), Length(min=14,max=14)])
    phonenumber = StringField('Phone Number',
                        validators=[DataRequired(), Length(min=11, max=14)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = session.query(User).filter_by(email=email.data).first()
        if user:
            raise ValidationError('That Email is taken. Please choose a different one.')

    def validate_nationalid(self, nationalid):
        user = session.query(User).filter_by(national_id=nationalid.data).first()
        if user:
            raise ValidationError('That National ID is taken. Please choose a different one.')

    def validate_phonenumber(self, phonenumber):
        user = session.query(User).filter_by(phone_num=phonenumber.data).first()
        if user:
            raise ValidationError('That Phone Number is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    fname = StringField('First Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    lname = StringField('Last Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    nationalid = StringField('National ID',
                        validators=[DataRequired(), Length(min=14,max=14)])
    phonenumber = StringField('Phone Number',
                        validators=[DataRequired(), Length(min=11, max=14)])

    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = session.query(User).filter_by(email=email.data).first()
            if user:
                raise ValidationError('That Email is taken. Please choose a different one.')
            

    def validate_nationalid(self, nationalid):
        if nationalid.data != current_user.national_id:
            user = session.query(User).filter_by(national_id=nationalid.data).first()
            if user:
                raise ValidationError('That National ID is taken. Please choose a different one.')

    def validate_phonenumber(self, phonenumber):
        if phonenumber.data != current_user.phone_num:
            user = session.query(User).filter_by(phone_num=phonenumber.data).first()
            if user:
                raise ValidationError('That Phone Number is taken. Please choose a different one.')
