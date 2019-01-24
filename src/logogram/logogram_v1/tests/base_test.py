from django.test import TestCase


class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
