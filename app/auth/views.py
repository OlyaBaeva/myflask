from threading import Thread

from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, current_user, login_required

from .forms import LoginForm, RegForm
from . import auth
from .. import db
from flask_mail import Message
from .. import mail
from ..decorators import permission_required
from ..models import User, Permission, Answer


@auth.before_app_request
def before_request():
    """
    The before_request function is executed before each request is processed by the Flask application.
    It checks whether the current user is logged in, whether his account is verified, and whether the requested URL is
    part of the auth module (authentication module) or a static file.
    If all these conditions are met,
    :return: redirect to the unconfirmed page defined in the auth module.
    """
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route("/quest")
def quest():
    """
    Function to determine whether a user has a registration on the site
    :return: render template for question
    """
    return render_template('Question.html')


@auth.route("/login", methods=['GET', 'POST'])
def login():
    """
    Function for logging in
    if the login form is validate_on_submit, we find the user in the database and check his password,
    after checking, the user is logged
    :return: redirect for next page
    else:
    :return: render template for 'login.html'
    """
    form = LoginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)


@auth.route("/unconfirmed")
def unconfirmed():
    """
    Function of blocking browsing for unverified users
    :return: phrase "Not confirmed. Unfortunately"
    """
    return "Not confirmed. Unfortunately"


@auth.route("/delete/<id>")
@login_required
@permission_required(Permission.MODERATE)
def delete(id):
    """
    Function for deleting comments only for users with permission MODERATE
    :param id: id for comment to delete
    Find comment this required id and delete it from database
    :return: redirect to the 'main.view_req'
    """
    comment = Answer.query.get(id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('main.view_req'))


@auth.route("/logout")
def logout():
    """
    Function for logging out
    :return: redirect to the main page
    """
    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    """
    Function for checking confirmation token
    :param token: confirmation token
    if user has already confirmed :return: redirect for main page
    if token matches the token assigned to current_user, the confirmation is successful
    else: link is not valid or not belong to current_user
    :return: redirect for main page
    """
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token.encode('utf-8')):
        db.session.commit()
        flash('Your confirmation was successful.')
    else:
        flash('Your link is not valid.', 'error')
    return redirect(url_for('main.index'))


@auth.route('/send_email')
def send_email():
    """
    Function for getting information about recipient to send email with registration token to the user
    :return: redirect to the main page
    """
    recipient = session.get('email')
    name = session.get('name')
    phone = session.get('phone')
    user = User.query.filter_by(username=name).first()
    token = user.generate_confirmation_token()
    msg = Message('Subject', sender=current_app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.body = render_template('confirm.txt', user=user, token=token.decode('utf-8'))
    from app_file import an_app
    thread = Thread(target=send_async_email, args=[an_app, msg])
    thread.start()
    return redirect(url_for('main.index'))


def send_async_email(app, msg):
    """
    Function for sending async email to the user
    :param app: current_app
    :param msg: message to send
    """
    with app.app_context():
        mail.send(msg)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registration function
    if the registration form is validate_on_submit, we check the presence of the user in the database and update
    it with new fields (nickname, password) and call the method of sending the letter,
    :return:  redirect for method 'auth.login'
    else:
    :return:  render template for 'register.html'
    """
    form = RegForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.confirmed:
                flash('You are already registered')
                return redirect(url_for('auth.login'))
            user.nick = form.nick.data
            user.password = form.password.data
            db.session.commit()
            send_email()
            flash('You can now login')
            return redirect(url_for('auth.login'))
        else:
            flash("Unfortunately you can't register", 'error')
    return render_template('register.html', form=form)
