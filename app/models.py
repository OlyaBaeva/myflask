from authlib.jose import JsonWebSignature
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login_manager


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMINISTER = 16


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
    description = db.Column(db.Text(), nullable=False)
    photo = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<Event %r>' % self.name


class Apartment(db.Model):
    __tablename__ = 'apartment'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    photo = db.Column(db.String(255), unique=True, nullable=False)
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return '<Apartment %r>' % self.Name


class Dishes(db.Model):
    __tablename__ = 'dish'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    photo = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return '<Dish %r>' % self.name


class Answer(db.Model):
    __tablename__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, index=True)
    phone = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    nick = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    mes = db.Column(db.Text(), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1)
    phone = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    nick = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    def init(self, *kwargs):
        super(User, self).init(*kwargs)
        if self.role is None or self.role == '':
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_admin(self):
        return self.can(Permission.ADMINISTER)

    def generate_confirmation_token(self):
        jws = JsonWebSignature()
        protected = {'alg': 'HS256'}
        payload = self.id
        secret = 'secret'
        return jws.serialize_compact(protected, payload, secret)

    def confirm(self, token):
        jws = JsonWebSignature()
        data = jws.deserialize_compact(s=token, key='secret')
        if data.payload.decode('utf-8') != str(self.id):
            print("it's not your token")
            return False
        else:
            self.confirmed = True
            db.session.add(self)
            return True

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


class Reservation(db.Model):
    __tablename__ = 'reserve'
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    since = db.Column(db.TIMESTAMP(timezone=False))
    forend = db.Column(db.TIMESTAMP(timezone=False))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN]
        }
        default_role = "User"
        for r in roles.keys():
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def has_permission(self, perm):
        return self.permissions & int(perm) == int(perm)

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0


class AnonymousUser(AnonymousUserMixin):
    def can(self, perm):
        return False

    def is_admin(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.anonymous_user = AnonymousUser
