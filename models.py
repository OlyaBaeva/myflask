from app import db

class Bar(db.Model):
    __tablename__ = 'cocktails'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    ingredients = db.Column(db.Text(), unique=True, nullable=False)
    volume = db.Column(db.Integer, unique=False, nullable=False)

def __repr__(self):
	return '<Cocktail %r>' % self.name