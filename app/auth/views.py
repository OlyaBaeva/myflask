from threading import Thread

from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, current_user, login_required

from .forms import LoginForm, RegForm
from . import auth
from .. import db
from flask_mail import Message
from .. import mail
from ..models import User

@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.blueprint != 'auth' \
        and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))
@auth.route("/quest")
def quest():
    return render_template('Question.html')


@auth.route("/login", methods=['GET', 'POST'])
def login():
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
    return "Not confirmed. Unfortunately"
@auth.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token.encode('utf-8')):
        db.session.commit()
        flash('Your confirmation was successful.')
    else:
        flash('Your link in not valid.')
    return redirect(url_for('main.index'))


@auth.route('/send_email')
def send_email():
    recipient = session.get('email')
    name = session.get('name')
    phone = session.get('phone')
    message = session.get('mes')
    if User.query.filter_by(username=name).first() is None:
        new_user = User(username=name, phone=phone, email=recipient)
        db.session.add(new_user)
        db.session.commit()
    user = User.query.filter_by(username=name).first()
    token = user.generate_confirmation_token()
    msg = Message('Subject', sender=current_app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.body = render_template('confirm.txt', user=user, token=token.decode('utf-8'))
    from app_file import an_app
    thread = Thread(target=send_async_email, args=[an_app, msg])
    thread.start()
    return redirect(url_for('main.index'))


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            user.nick = form.nick.data
            user.password = form.password.data
            db.session.commit()
            flash('You can now login')
            return redirect(url_for('auth.login'))
        else:
            flash("Unfortunately you can't register", 'error')

    return render_template('register.html', form=form)
