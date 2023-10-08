from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,DateField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[
                            DataRequired(message="E-mail can not be empty"),
                            Email()])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(message="Password can not be empty"),
                                 Length(min=6, max=25, message='Password length is 6-25 characters'),
                             ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[
                               DataRequired(message="Username can not be empty"),
                               Length(min=2, max=20, message='Username length is 2-20 characters')
                           ])
    email = StringField('Email',
                        validators=[
                            DataRequired(message="Email can not be empty"),
                            Email(message="Invalid email address")
                        ])
    password = PasswordField('Password',
                             validators=[
                                 DataRequired(message="Password can not be empty"),
                                 Length(min=6, max=25, message='Password length is 6-25 characters')
                             ])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[
                                         DataRequired(message="Please confirm your password"),
                                         EqualTo('password', message="Passwords must match")
                                     ])
    submit = SubmitField('Register')

class SettingForm(FlaskForm):
    password = PasswordField('Original password',
                             validators=[
                                 DataRequired(message="Original password can not be empty"),
                                 Length(min=6, max=25, message='Password length is 6-25 characters'),
                             ])
    new_password = PasswordField('New password',
                                 validators=[
                                     DataRequired(message="New password can not be empty"),
                                     Length(min=6, max=25, message='Password length is 6-25 characters')])
    confirm_password = PasswordField('Confirm password',
                                     validators=[
                                         DataRequired(message="Confirm password can not be empty"),
                                         EqualTo('new_password', message="The passwords entered twice are inconsistent")])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
class AddRoutineForm(FlaskForm):
    details = TextAreaField('Routine description',
                                   validators=[
                                       DataRequired(message="Routine content is required"),
                                       Length(max=255, message='Routine content should be at most 255 characters')
                                   ])
    submit = SubmitField('Add Routine')
class InfoForm(FlaskForm):
    username = StringField('Name',
                            validators=[
                                DataRequired(message="Name can not be empty"),
                                Length(min=2, max=60, message='Password length is 6-25 characters'),
                            ],
                            render_kw={'class': 'form-control','readonly': True}
                           )

