from flask import request, render_template, session, redirect, url_for, flash
from flask_login import current_user
from . import main
from .forms import MyForm, ReviewForm
from app.models import *
from datetime import datetime


@main.app_context_processor
def inject_permission():
    """
    The inject_permission function, which is represents the processor of the application context.
    It adds the Permission variable to the template context for all views in the main module.
    :return: dict of permissions from model Permission
    """
    return dict(Permission=Permission)


@main.route("/bar", methods=['GET'])
def bar():
    """
    Function for getting all cocktails from bd
    :return: render template for bar with all cocktails
    """
    cocktails = Bar.query.all()
    return render_template('Bar.html', cocktails=cocktails)


@main.route("/activity", methods=['GET'])
def activity():
    """
    Function for getting all events from bd
    :return: render template for activities with all events
    """
    events = Event.query.all()
    return render_template('Activities.html', events=events)


@main.route("/walks", methods=['GET', 'POST'])
def walking():
    """
    Function for view page about walking in space
    :return: render template for walking
    """
    return render_template('Walks.html')


def date_times(input_date_time1):
    """
    Function for converting a string date to a save format in a database
    :param input_date_time1: string date
    :return: if the date matches the format %m/%d/%Y, the datetime object is returned,
    otherwise we return an empty string
    """
    try:
        datetime1 = datetime.strptime(input_date_time1, '%m/%d/%Y')
        return datetime1
    except:
        return ""


@main.route("/reserve", methods=['GET', 'POST'])
def reserve():
    """
    Function is used to handle requests for reserving apartments.
    If the request method is GET,
    :return: renders the reserve.html template with the retrieved apartments from the database and created form
    else:
        If the submit_review button was clicked:
            it performed string datas to the right format, checks if the dates are valid and
            if the start date is before the end date.
            stores the dates in the session.
           :return: the reserve.html template
        else:
            Extracts the user's name, email, and phone number from the form data.
            Checks if a user with the given name already exists in the database.
            If the user does not exist, creates a new user record and adds it to the database.
            Creates a new reservation record with the apartment name, user email, start date,
            and end date and adds it to the database
            :return: Render the booking.html template .
        Retrieves all reservation records from the database.
        Parses the since and for dates from the form data.
        Creates a list of available apartments by checking which apartments
        are not already booked for the specified dates.
        :return: the reserve.html template with the list of available apartments and the form.
    """

    apartments = Apartment.query.all()
    form = MyForm()
    if request.method == "GET":
        return render_template('reserve.html')
    else:
        if request.form.get('submit_review') is not None:
            since = date_times(request.form['since'])
            forend = date_times(request.form['for'])
            if since != "" and forend != "" and since < forend:
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
    """
    Function for booking the room
    :param info: name of room
    :return: if the user is logged in without additional data,
    the booking takes place and the render template for "success", else this is redirected to 'main.reserve'
    """
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
    """
    Function for getting all dishes from bd
    :return: render template for Restaurant with all dishes
    """
    dishes = Dishes.query.all()
    return render_template('Restaurant.html', dishes=dishes)


@main.route("/", methods=['GET', 'POST'])
def index():
    """
    Function for view main page
    :return: render template for main page
    """
    return render_template('poruchik.html')


@main.route('/req', methods=['GET', 'POST'])
def view_req():
    """
    Function for sending and viewing reviews
    :return:  If the method "GET", it returns all reviews from database
    and render template with form for creating new one,
    otherwise, it :return: redirect to the view_req function,
    taking into account the new review created and added to the database
    """
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
