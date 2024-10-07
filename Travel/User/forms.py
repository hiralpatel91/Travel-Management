from flask_wtf import FlaskForm
from wtforms import  StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError,Email,Optional
from Travel.User.models import User  # Import your User model
from flask_login import current_user

# create form for user register, login and update profile
class UserSignUpForm(FlaskForm):
    username = StringField('Username: ', 
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    email = StringField('Email: ', 
                        validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control","type": "email"})
    password = PasswordField('Password: ', 
                             validators=[EqualTo('confirm', message='Both Password Must Match!')],
                             render_kw={"class": "form-control"})
    confirm = PasswordField('Confirm Password: ', 
                            validators=[],
                            render_kw={"class": "form-control"})
    submit = SubmitField('Register', 
                         render_kw={"class": "btn btn-primary"})


    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("This Username is already in use!")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This Email is already in use!")
        

class UserSigninForm(FlaskForm):
    email = StringField('Email: ', 
                        validators=[DataRequired()],
                        render_kw={"class": "form-control"})
    password = PasswordField('Password: ', 
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    

class UserProfileUpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional()])
    confirm_password = PasswordField('Confirm New Password', 
                                      validators=[Optional(), EqualTo('new_password', message='Passwords must match.')])
    submit = SubmitField('Update')

    def validate_new_password(form, field):
        if field.data and not form.current_password.data:
            raise ValidationError('Current password is required when changing the password.')

    