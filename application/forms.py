from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from application.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account with that email address already exists. '
                                    + 'Please reset your password or sign up with a different email.')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class ApplicationForm(FlaskForm):
    company = TextAreaField('Company name', validators=[
        DataRequired(), Length(min=1, max=140)])
    position = TextAreaField('Position', validators=[
        DataRequired(), Length(min=1, max=140)])
    status = SelectField(
        'Current Application Status',
        choices=[('Applied', 'Applied'), ('Interviewing', 'Interviewing'), ('Offer', 'Offer'), ('Rejected', 'Rejected')]
    )
    submit = SubmitField('Submit')

class UpdateApplicationForm(FlaskForm):
    status = SelectField(
        'Application Status',
        choices=[('Applied', 'Applied'), ('Interviewing', 'Interviewing'), ('Offer', 'Offer'), ('Rejected', 'Rejected')]
    )
    submit = SubmitField('Update')

    def __init__(self, original_status, *args, **kwargs):
        super(UpdateApplicationForm, self).__init__(*args, **kwargs)
        self.original_status = original_status

    def validate_status(self, username):
        if self.original_status == self.status.data:
            raise ValidationError('You chose the same status as is currently stored.')

class DeleteApplicationForm(FlaskForm):
    delete = SelectField(
        'Are you sure you would like to delete this application?',
        choices=[('No', 'No'), ('Yes', 'Yes')]
    )
    submit = SubmitField('Delete')
