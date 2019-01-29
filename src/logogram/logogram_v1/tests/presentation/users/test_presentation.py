"""Test entity creation and persistence of the Users entity """
from logogram_v1.tests.base_test import BaseTestCase
from logogram_v1.domain_persistence.users.models import Users
from logogram_v1.presentation.users.users import UsersDetailView
from rest_framework.exceptions import PermissionDenied


class UsersViewPresentation(BaseTestCase):

    def setUp(self):
        super(UsersViewPresentation, self).setUp()
        self.user_data = {"first_name": "Pinocchio", "last_name": "Cartoon",
                          "email": "pinocchio@gmail.com",
                          "password": "password"}
        self.post_user_response = self.client.post(
            "/api/v1/users/", self.user_data)

    def test_post_user(self):
        """
        Test that you can post a user to the /users/ view and
            - get a 201 status code.
            - get a response containing the data we had just posted.
        """
        self.assertEqual(self.post_user_response.status_code, 201)
        self.assertIn(self.user_data["first_name"],
                      self.post_user_response.content.decode("utf-8"))
        self.assertIn(self.user_data["last_name"],
                      self.post_user_response.content.decode("utf-8"))
        self.assertIn(self.user_data["email"],
                      self.post_user_response.content.decode("utf-8"))

    def test_get_users(self):
        """
        Test that you can submit a GET request to the /users/ path and
            - get a 200 status code.
            - get a response containing a list of users.
        """
        get_users_response = self.client.get("/api/v1/users/")
        self.assertEqual(get_users_response.status_code, 200)
        self.assertIn(self.user_data["first_name"],
                      get_users_response.content.decode("utf-8"))
        self.assertIn(self.user_data["last_name"],
                      get_users_response.content.decode("utf-8"))
        self.assertIn(self.user_data["email"],
                      get_users_response.content.decode("utf-8"))


class UsersDetailPresentation(BaseTestCase):

    def setUp(self):
        super(UsersDetailPresentation, self).setUp()

    def test_get_a_user_who_exists(self):
        """
        Test that when you make a get request on the /users/pk/ route
            - that you get a user who already exists in database
            - That the password of the user is not rendered
        """
        Users.objects.create(email="simpsons@gmail.com", first_name="Homer",
                             last_name="Simpsons", password="my_password")
        user = Users.objects.get(email="simpsons@gmail.com")
        self.client.force_login(user)
        get_user_response = self.client.get(
            "/api/v1/users/{}/".format(user.id))
        self.assertEqual(get_user_response.status_code, 200)
        self.assertIn(user.first_name,
                      get_user_response.content.decode("utf-8"))
        self.assertIn(user.last_name,
                      get_user_response.content.decode("utf-8"))
        self.assertIn(user.email, get_user_response.content.decode("utf-8"))
        self.assertNotIn("my_password",
                         get_user_response.content.decode("utf-8"))

    def test_permission_error_if_not_logged_in(self):
        """
        Test that accessing the /users/pk route without logging in
            - will raise an error
        """
        Users.objects.create(email="simpsons@gmail.com", first_name="Homer",
                             last_name="Simpsons", password="my_password")
        user = Users.objects.get(email="simpsons@gmail.com")
        response = self.client.get("/api/v1/users/{}/".format(user.id))
        authentication_error = "Authentication credentials were not provided"
        self.assertEqual(response.status_code, 403)
        self.assertIn(authentication_error, response.content.decode("utf-8"))

    def test_permission_error_accessing_other_users_details(self):
        """
        Test that when accessing the /users/pk/ route and the route determines
        that the one accessing the details wants to view another users details
            - That an error is raised
        """
        Users.objects.create(email="simpsons@gmail.com", first_name="Homer",
                             last_name="Simpsons", password="my_password")
        simpsons = Users.objects.get(email="simpsons@gmail.com")
        Users.objects.create(email="clark@gmail.com", first_name="Clark",
                             last_name="Kent", password="my_password")
        clark = Users.objects.get(email="clark@gmail.com")
        self.client.force_login(simpsons)
        response = self.client.get("/api/v1/users/{}/".format(clark.id))
        authentication_error = ('You do not have permission to perform this'
                                ' action.')
        self.assertEqual(response.status_code, 403)
        self.assertIn(authentication_error, response.content.decode("utf-8"))

    def test_permission_error_raised_check_id(self):
        """
        Test error raised when numbers are not similar
        """
        with self.assertRaises(PermissionDenied):
            UsersDetailView().check_pk_similar_to_user_id(2, 3)
