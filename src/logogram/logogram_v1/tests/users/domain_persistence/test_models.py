'''Test entity creation and persistence of the Users entity '''
from logogram_v1.tests.base_test import BaseTestCase
from logogram_v1.domain_persistence.users.models import Users
from django.db import IntegrityError

class UsersModel(BaseTestCase):

    def setUp(self):
        super(UsersModel, self).setUp()
        self.name = ("longnameexampleinfirstandlastnameinput")

    def test_email_attribute_uniqueness(self):
        '''
        Test that the email attribute for the Users model:
            - is unique, an integrity error should be raised by the database
        '''
        Users.objects.create(email="example@gmail.com")
        with self.assertRaises(IntegrityError):
            Users.objects.create(email="example@gmail.com")
