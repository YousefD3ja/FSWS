from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Site.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=8)])
    confirm_password = PasswordField("Confirm Password", 
                                     validators=[DataRequired(),Length(min=8), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("username already taken.")
    
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("email already taken.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("", validators=[FileAllowed(['png', 'jpg'])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            if User.query.filter_by(username=username.data).first():
                raise ValidationError("username already taken.")
            
    
    def validate_email(self, email):
        if email.data != current_user.email:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("email already taken.")
            
class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Requset Reset Password")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first() == None:
            raise ValidationError("email does not exist!")
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(),Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(),Length(min=8), EqualTo('password')])
    submit = SubmitField("Reset")