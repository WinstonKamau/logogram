"""Test entity creation and persistence of the Users entity """
from logogram_v1.tests.base_test import BaseTestCase
from logogram_v1.domain_persistence.users.models import Users, UserManager
from django.db import IntegrityError


class UsersModel(BaseTestCase):

    def setUp(self):
        super(UsersModel, self).setUp()
        self.name = ("longnameexampleinfirstandlastnameinput")

    def test_email_attribute_uniqueness(self):
        """
        Test that the email attribute for the Users model:
            - is unique, an integrity error should be raised by the database
        """
        Users.objects.create(email="example@gmail.com")
        with self.assertRaises(IntegrityError):
            Users.objects.create(email="example@gmail.com")


class UserManagerTestCase(BaseTestCase):

    def test_create_user(self):
        email_lowercase = 'normal@normal.com'
        user = Users.objects.create_user(email_lowercase)
        self.assertEqual(user.email, email_lowercase)
        self.assertFalse(user.has_usable_password())

    def test_create_user_email_domain_normalize_rfc3696(self):
        # According to https://tools.ietf.org/html/rfc3696#section-3
        # the "@" symbol can be part of the local part of an email address
        returned = UserManager.normalize_email(r'Abc\@DEF@EXAMPLE.com')
        self.assertEqual(returned, r'Abc\@DEF@example.com')

    def test_create_user_email_domain_normalize(self):
        returned = UserManager.normalize_email('normal@DOMAIN.COM')
        self.assertEqual(returned, 'normal@domain.com')

    def test_create_user_email_domain_normalize_with_whitespace(self):
        returned = UserManager.normalize_email(r'email\ with_whitespace@D.COM')
        self.assertEqual(returned, r'email\ with_whitespace@d.com')

    def test_create_user_is_staff(self):
        email = 'normal@normal.com'
        user = Users.objects.create_user(email, is_staff=True)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_staff)

    def test_create_super_user_raises_error_on_false_is_superuser(self):
        message = "Superuser must have is_superuser=True."
        with self.assertRaisesMessage(ValueError, message):
            Users.objects.create_superuser(
                username='test', email='test@test.com',
                password='test', is_superuser=False,
            )

    def test_create_superuser_raises_error_on_false_is_staff(self):
        message = "Superuser must have is_staff=True."
        with self.assertRaisesMessage(ValueError, message):
            Users.objects.create_superuser(
                email='test@test.com', password='test', is_staff=False,
            )

    def test_make_random_password(self):
        allowed_chars = 'abcdefg'
        password = UserManager().make_random_password(5, allowed_chars)
        self.assertEqual(len(password), 5)
        for char in password:
            self.assertIn(char, allowed_chars)
