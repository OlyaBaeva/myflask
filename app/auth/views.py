from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user

from .forms import LoginForm, RegForm
from . import auth
from .. import db
from ..models import User


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


@auth.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


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
