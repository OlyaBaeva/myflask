import unittest

from app.models import *


class UserModelTestCase(unittest.TestCase):
    def test_anon(self):
        Role.insert_roles()
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.ADMIN))
        self.assertFalse(user.can(Permission.MODERATE))
        self.assertFalse(user.can(Permission.FOLLOW))
        self.assertFalse(user.can(Permission.WRITE))
        self.assertFalse(user.can(Permission.COMMENT))

    def test_user_role(self):
        Role.insert_roles()
        user = User(email='olyabaewa2014@mail.ru', username="Olya", phone='8989876655')
        self.assertFalse(user.can(Permission.ADMIN))
        self.assertFalse(user.can(Permission.MODERATE))
        self.assertTrue(user.can(Permission.FOLLOW))
        self.assertTrue(user.can(Permission.COMMENT))
        self.assertTrue(user.can(Permission.WRITE))
