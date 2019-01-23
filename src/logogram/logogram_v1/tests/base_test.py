import os
from django.test import TestCase, Client

class BaseTestCase(TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
