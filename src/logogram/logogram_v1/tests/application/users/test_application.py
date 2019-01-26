"""Test entity creation and persistence of the Users entity """
from logogram_v1.tests.base_test import BaseTestCase
from logogram_v1.application.users.users import UsersSerializer


class UsersApplication(BaseTestCase):

    def setUp(self):
        super(UsersApplication, self).setUp()
        self.serializer_data = UsersSerializer().data
        self.serializer_data_2 = UsersSerializer().data
        self.normal_name_length = "shortname"

    def test_users_serializer_class(self):
        """
        Test that the User Serializer class contains the required fields.
        """
        self.assertEqual(set(self.serializer_data.keys()),
                         set(['first_name', 'last_name', 'email', 'password']))

    def test_users_serializer_attribute_length(self):
        """
        Test that the first_name attribute on a User Serializer class will
        raise an invalid attribute when:
            - The length of the first_name is greater than thirty characters.
        """
        long_name_length = "afirstnamegreatherthanthirtycharacters"
        normal_email_length = "example@gmail.com"
        self.serializer_data['first_name'] = self.normal_name_length
        self.serializer_data['last_name'] = self.normal_name_length
        self.serializer_data['email'] = normal_email_length
        self.serializer_data['password'] = "password"
        serializer = UsersSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        self.serializer_data_2['first_name'] = long_name_length
        self.serializer_data_2['last_name'] = long_name_length
        self.serializer_data_2['email'] = normal_email_length
        self.serializer_data['password'] = "password"
        serializer_2 = UsersSerializer(data=self.serializer_data_2)
        self.assertFalse(serializer_2.is_valid())
        name_error_message = ('Ensure this field has no more than '
                              '30 characters.')
        self.assertIn(name_error_message, serializer_2.errors["first_name"])
        self.assertIn(name_error_message, serializer_2.errors["last_name"])
        self.assertIsNone(serializer_2.errors.get("email"))

    def test_users_serializer_attribute_blank(self):
        """
        Test that the first_name, last_name and email attribute on a User
        Serializer class will:
            - raise an invalid attribute when the attribute is blank
        """
        self.serializer_data['first_name'] = ""
        self.serializer_data['last_name'] = ""
        self.serializer_data['email'] = ""
        serializer = UsersSerializer(data=self.serializer_data)
        self.assertFalse(serializer.is_valid())
        blank_error_message = "This field may not be blank."
        self.assertIn(blank_error_message, serializer.errors["first_name"])
        self.assertIn(blank_error_message, serializer.errors["last_name"])
        self.assertIn(blank_error_message, serializer.errors["email"])
        self.assertIn(blank_error_message, serializer.errors["password"])

    def test_email_uniqueness(self):
        """
        Test that the email attribute is unique and cannot be added twice
        """
        self.serializer_data['first_name'] = self.normal_name_length
        self.serializer_data['last_name'] = self.normal_name_length
        self.serializer_data['email'] = "example@gmail.com"
        self.serializer_data['password'] = "password"
        serializer = UsersSerializer(data=self.serializer_data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.serializer_data_2['first_name'] = self.normal_name_length
        self.serializer_data_2['last_name'] = self.normal_name_length
        self.serializer_data_2['email'] = "example@gmail.com"
        self.serializer_data['password'] = "password"
        serializer_2 = UsersSerializer(data=self.serializer_data_2)
        self.assertFalse(serializer_2.is_valid())
        email_error_message = ('The email address you entered has already '
                               'been registered.')
        self.assertIn(email_error_message, serializer_2.errors["email"])
