from flask import flash, redirect, render_template, url_for
from flask.globals import current_app
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
from ..admin.views import send_mail_reset
from .forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, ProfileForm
from .. import db
from ..models import User

@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Este e-mail não existe!', 'danger')
        else:
            token = user.get_reset_password_token()
            send_mail_reset(token, user)
            flash('Verifique sua caixa de e-mail. Enviamos um link para redefinir senha', 'success')

    # load registration template
    return render_template('auth/reset_password_request.html', form=form, title='Resetar Password')

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('auth:login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the /register route
    Add an user to the database through the registration form
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        # add user to the database
        db.session.add(user)
        db.session.commit()
        logout_user()
        flash('Você se registrou com sucesso! Agora você pode fazer o login.', 'success')

        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load registration template
    return render_template('auth/register.html', form=form, title='Register')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an user in through the login form
    """
    form = LoginForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log user in
            login_user(user)

            # redirect to the dashboard page after login
            return redirect(url_for('home.homepage'))

        # when login details are incorrect
        else:
            flash('E-mail ou senha inválidos.', 'danger')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an user out through the logout link
    """
    logout_user()
    flash('Você foi desconectado com sucesso.', 'primary')

    # redirect to the login page
    return redirect(url_for('auth.login'))

@auth.route('/profile')
@login_required
def profile():
    """
    Handle requests to the /profile route
    Log an user out through the logout link
    """
    form = ProfileForm()
    if form.validate_on_submit():

        # check whether user exists in the database and whether
        # the password entered matches the password in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(
                form.password.data):
            # log user in
            login_user(user)

            # redirect to the dashboard page after login
            return redirect(url_for('home.homepage'))

        # when login details are incorrect
        else:
            flash('E-mail ou senha inválidos.')

    # load login template
    return render_template('auth/profile.html', form=form, title='Profile')