from flask import Flask, request, make_response, render_template, session, redirect, url_for
from flask_mail import Message

from app import an_app, mail

from app.forms import MyForm
from models import Bar


@an_app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@an_app.route("/form")
def form_app(name=None):
        return render_template('form.html')
@an_app.route("/bar", methods=['GET', 'POST'])
def bar(name=None):
    cocktails = Bar.query.all()
    return render_template('Bar.html', cocktails=cocktails)
@an_app.route("/activity", methods=['GET','POST'])
def activity():
    return render_template('Activities.html')

@an_app.route("/", methods=['GET', 'POST'])
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


@an_app.route('/send_email')
def send_email():
    recipient = session.get('email')
    name = session.get('name')
    phone = session.get('phone')
    message = session.get('mes')
    msg = Message('Subject', sender=an_app.config['MAIL_USERNAME'], recipients=[recipient])
    msg.html = render_template('email.html', name=name, email=recipient, phone=phone, message=message)

    mail.send(msg)
    return 'Email sent to ' + recipient