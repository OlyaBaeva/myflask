from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class Bar(db.Model):
    __tablename__ = 'cocktails'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    ingredients = db.Column(db.Text(), unique=True, nullable=False)
    volume = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
       return '<Cocktail %r>' % self.name

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text(),  nullable=False)
    photo = db.Column(db.String(255), unique=True, nullable=False)
    def __repr__(self):
        return '<Event %r>' % self.name

class Apartment(db.Model):
    __tablename__ = 'apartment'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text(),  nullable=False)
    photo = db.Column(db.String(255), unique=True, nullable=False)
    def __repr__(self):
        return '<Apartment %r>' % self.name

class Dishes(db.Model):
    __tablename__ = 'dish'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text(),  nullable=False)
    photo = db.Column(db.String(255), unique=True, nullable=False)
    def __repr__(self):
        return '<Dish %r>' % self.name

class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(50), nullable=False, index = True)
    phone =db.Column(db.String(200), nullable=False)
    email =db.Column(db.String(200), nullable=False)
    nick = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    mes = db.Column(db.Text(),  nullable=False)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index = True)
    phone = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    nick = db.Column(db.String(50),  unique=True)
    password_hash = db.Column(db.String(128))
    @property
    def password(self):
     raise AttributeError("password not enable to read")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def verify(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

