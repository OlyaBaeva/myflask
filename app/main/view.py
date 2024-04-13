from flask import request, render_template, session, redirect, url_for, current_app
from flask_login import current_user
from flask_mail import Message

from . import main
from .forms import MyForm, ReviewForm
from .. import mail
from app.models import *


@main.route("/form")
def form_app():
    return render_template('form.html')


@main.route("/bar", methods=['GET', 'POST'])
def bar():
    cocktails = Bar.query.all()
    return render_template('Bar.html', cocktails=cocktails)


@main.route("/activity", methods=['GET', 'POST'])
def activity():
    events = Event.query.all()
    return render_template('Activities.html', events=events)


@main.route("/menu", methods=['GET', 'POST'])
def restaurant():
    dishes = Dishes.query.all()
    return render_template('Restaurant.html', dishes=dishes)


@main.route("/", methods=['GET', 'POST'])
def index():
    if 'name' in session:
        name = session['name']
        email = session['email']
        phone = session['phone']
    else:
        name = None
        email = None
        phone = None
    mes = None
    form = MyForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['email'] = form.email.data
        session['phone'] = form.phone.data
        session['mes'] = form.message.data
        return redirect(url_for('.send_email'))
    return render_template('poruchik.html', form=form, name=name, email=email, phone=phone, message=mes)


@main.route('/send_email')
def send_email():
    recipient = session.get('email')
    name = session.get('name')
    phone = session.get('phone')
    message = session.get('mes')
    msg = Message('Subject', sender=current_app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.html = render_template('email.html', name=name, email=recipient, phone=phone, message=message)
    if User.query.filter_by(username=name).first() is None:
        new_user = User(username=name, phone=phone, email=recipient)
        db.session.add(new_user)
        db.session.commit()
    mail.send(msg)
    return 'Email sent to ' + recipient


@main.route('/req', methods=['GET', 'POST'])
def view_req():
    if request.method == 'GET':
        ans = Answer.query.all()
        form = ReviewForm()
        return render_template('req.html', ans=ans, form=form)
    else:
        mes = request.form['message']
        user=current_user
        new_answer = Answer(username=user.username, phone=user.phone, email=user.email, nick=user.nick,
                            password_hash=user.password_hash, mes=mes)
        db.session.add(new_answer)
        db.session.commit()
        return redirect(url_for('.view_req'))

'''''
@main.route('/leave_review', methods=['GET', 'POST'])
def post_req():
    print(session.get('email'))
    email = session.get('email')
    if email is not None:
        user = User.query.filter_by(email=email)
        ans = Answer.query.all()
        form = ReviewForm()
        if user.is_authenticated:
            return redirect(url_for('.req'))
        return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.register'))



@main.route('/leave_review', methods=['GET', 'POST'])
@login_required
def leave_review():
    email = session.get('email')
    user = User.query.filter_by(email=email).first()
    ans = Answer.query.filter_by(email=email).first()
    if ans is not None:
        nick = ans.nick
        if request.method == 'POST':
           password = request.form['password']
           mes = request.form['message']
           if user.verify(password):
               new_answer =Answer(username=user.username, phone=user.phone, email=user.email, nick=nick, password_hash=user.password_hash, mes = mes)
               db.session.add(new_answer)
               db.session.commit()
               return redirect(url_for('.requests'))
           else:
               return "Неверный пароль"
        else:
            return render_template('leave_review.html', nick=nick, password=user.password_hash)
    else:
        if request.method == 'POST':
           nick = request.form['nickname']
           password = request.form['new_password']
           password2 = request.form['check_password']
           mes = request.form['message']
           if password!=password2:
               return "Не совпадение пароля"
           else:
               user.nick = nick
               user.password=password
               new_answer=Answer(username=user.username, phone=user.phone, email=user.email, nick=nick, password_hash=user.password_hash, mes=mes)
               db.session.add(new_answer)
               db.session.commit()
               return redirect(url_for('.requests'))
        else:
            return render_template('leave_review.html')
'''''
