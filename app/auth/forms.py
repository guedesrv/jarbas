from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError, FormField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User, Company


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    email = StringField(label=None, validators=[DataRequired(), Email()], render_kw={'class':'fadeIn second', 'placeholder':'Email'})
    password = PasswordField(label=None, validators=[DataRequired()], render_kw={'class':'fadeIn third', 'placeholder':'Password'})
    submit = SubmitField('Login', render_kw={'class':'btn btn-primary'})

class ResetPasswordRequestForm(FlaskForm):
    """
    Form for users to reset password
    """
    email = StringField(label=None, validators=[DataRequired(), Email()], render_kw={'class':'fadeIn second', 'placeholder':'Email'})
    submit = SubmitField('Reset', render_kw={'class':'btn btn-primary'})

class ResetPasswordForm(FlaskForm):
    """
    Form for users to reset password
    """
    password = PasswordField(label=None, validators=[DataRequired()], render_kw={'class':'fadeIn third', 'placeholder':'Password'})
    repeat_password = PasswordField(label=None, validators=[DataRequired(), EqualTo('password')], render_kw={'class':'fadeIn third', 'placeholder':'Repeat Password'})
    submit = SubmitField('Request Password Reset', render_kw={'class':'btn btn-primary'})

class ProfileForm(FlaskForm):
    """
    Form for users to profile
    """
    companies = SelectMultipleField('Company', validators=[DataRequired()])
    # name = StringField(label='Nome', validators=[DataRequired()])
    # repeat_password = PasswordField(label=None, validators=[DataRequired(), EqualTo('password')], render_kw={'class':'fadeIn third', 'placeholder':'Repeat Password'})
    # submit = SubmitField('Request Password Reset', render_kw={'class':'btn btn-primary'})

    # def __init__(self, *args, **kwargs):
    #     super(ProfileForm, self).__init__(*args, **kwargs)
    #     self.companies.choices = [Company.query.filter(user_id)]

# class CompanyForm(FlaskForm):
#     class Meta:
#         model = Company
#         fields = ['id', 'name']


# class PerfilForm(FlaskForm):
#     choices = Company.query.all()
#     print(choices)
#     companies = SelectMultipleField('Ecommerce', choices=[choices])