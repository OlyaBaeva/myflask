from flask import Flask, request, make_response, render_template, session, redirect, url_for
from flask_mail import Message

from . import main
from .forms import MyForm
from .. import mail

from app.models import *



@main.route("/form")
def form_app(name=None):
        return render_template('form.html')
@main.route("/bar", methods=['GET', 'POST'])
def bar(name=None):
    cocktails = Bar.query.all()
    return render_template('Bar.html', cocktails=cocktails)
@main.route("/activity", methods=['GET','POST'])
def activity():
    events = Event.query.all()
    return render_template('Activities.html', events=events)
@main.route("/menu", methods=['GET','POST'])
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
      return redirect(url_for('send_email'))
    return render_template('poruchik.html', form=form, name=name, email=email, phone=phone, message=mes)


@main.route('/send_email')
def send_email():
    recipient = session.get('email')
    name = session.get('name')
    phone = session.get('phone')
    message = session.get('mes')
    msg = Message('Subject', sender=main.config['MAIL_USERNAME'], recipients=[recipient])
    msg.html = render_template('email.html', name=name, email=recipient, phone=phone, message=message)

    mail.send(msg)
    return 'Email sent to ' + recipient