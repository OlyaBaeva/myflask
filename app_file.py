import os
import unittest
from app import create_app, db
from app.models import *
an_app = create_app("default")
'''''
@an_app.shell_context_processors
def make_shell_context():
    return dict(db=db, Bar=Bar, Event=Event, Apartment=Apartment, Dishes=Dishes)
'''''
@an_app.cli.command('test')
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)