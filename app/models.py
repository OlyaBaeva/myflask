from . import db

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