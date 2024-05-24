from flask import request, render_template, session, redirect, url_for, flash
from flask_login import current_user
from . import main
from .forms import MyForm, ReviewForm
from app.models import *
from datetime import datetime


@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)


@main.route("/bar", methods=['GET', 'POST'])
def bar():
    cocktails = Bar.query.all()
    return render_template('Bar.html', cocktails=cocktails)


@main.route("/activity", methods=['GET', 'POST'])
def activity():
    events = Event.query.all()
    return render_template('Activities.html', events=events)


@main.route("/walks", methods=['GET', 'POST'])
def walking():
    return render_template('Walks.html')


def date_times(input_date_time1):
    try:
        datetime1 = datetime.strptime(input_date_time1, '%m/%d/%Y')
        return datetime1
    except:
        return ""


@main.route("/reserve", methods=['GET', 'POST'])
def reserve():
    apartments = Apartment.query.all()
    form = MyForm()
    if request.method == "GET":
        return render_template('reserve.html')
    else:
        if request.form.get('submit_review') is not None:
            since = date_times(request.form['since'])
            forend = date_times(request.form['for'])
            if since != "" and forend != "":
                session['since'] = since
                session['forend'] = forend
            else:
                flash('Неправильный формат даты, повторите, пожалуйста', 'error')
                return render_template('reserve.html')
        else:
            session['name'] = form.name.data
            session['email'] = form.email.data
            session['phone'] = form.phone.data
            if User.query.filter_by(username=form.name.data).first() is None:
                new_user = User(username=form.name.data, phone=form.phone.data, email=form.email.data)
                db.session.add(new_user)
            new_book = Reservation(name=form.NameApart.data, email=form.email.data, since=session['since'],
                                   forend=session['forend'])
            db.session.add(new_book)
            db.session.commit()
            return render_template('booking.html')
        reservation = Reservation.query.all()
        since = date_times(request.form['since'])
        forend = date_times(request.form['for'])
        free = []
        for apart in apartments:
            for reserve in reservation:
                if reserve.name == apart.Name:
                    num_reservations = Reservation.query.filter(Reservation.name == apart.Name).filter(
                        Reservation.since <= forend).filter(Reservation.forend >= since).count()
                    if apart not in free:
                        if reserve.forend < since or reserve.since > forend:
                            free.append(apart)
                        elif num_reservations < apart.quantity:
                            free.append(apart)
        for apartment in apartments:
            if apartment not in free:
                free.append(apartment)
        return render_template('reserve.html', apartments=free, form=form)


@main.route("/booking/<info>", methods=['POST'])
def book(info):
    since = session.get('since')
    forend = session.get('forend')
    if current_user.is_authenticated:
        email = current_user.email
        new_book = Reservation(name=info, email=email, since=since, forend=forend)
        db.session.add(new_book)
        db.session.commit()
        return render_template('booking.html')
    return redirect(url_for('main.reserve'))


@main.route("/menu", methods=['GET', 'POST'])
def restaurant():
    dishes = Dishes.query.all()
    return render_template('Restaurant.html', dishes=dishes)


@main.route("/", methods=['GET', 'POST'])
def index():
    return render_template('poruchik.html')


@main.route('/req', methods=['GET', 'POST'])
def view_req():
    if request.method == 'GET':
        ans = Answer.query.all()
        form = ReviewForm()
        return render_template('req.html', ans=ans, form=form)
    else:
        mes = request.form['message']
        user = current_user
        new_answer = Answer(username=user.username, phone=user.phone, email=user.email, nick=user.nick,
                            password_hash=user.password_hash, mes=mes)
        db.session.add(new_answer)
        db.session.commit()
        return redirect(url_for('.view_req'))
