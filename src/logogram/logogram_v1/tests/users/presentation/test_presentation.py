'''Test entity creation and persistence of the Users entity '''
from logogram_v1.tests.base_test import BaseTestCase
from logogram_v1.domain_persistence.users.models import Users


class UsersViewPresentation(BaseTestCase):

    def setUp(self):
        super(UsersViewPresentation, self).setUp()
        self.user_data = {"first_name": "Pinocchio", "last_name": "Cartoon",
                          "email": "pinocchio@gmail.com",
                          "password": "password"}
        self.post_user_response = self.client.post(
            "/api/v1/users/", self.user_data)

    def test_post_user(self):
        '''
        Test that you can post a user to the /users/ view and
            - get a 201 status code.
            - get a response containing the data we had just posted.
        '''
        self.assertEqual(self.post_user_response.status_code, 201)
        self.assertIn(self.user_data["first_name"],
                      self.post_user_response.content.decode("utf-8"))
        self.assertIn(self.user_data["last_name"],
                      self.post_user_response.content.decode("utf-8"))
        self.assertIn(self.user_data["email"],
                      self.post_user_response.content.decode("utf-8"))

    def test_get_users(self):
        '''
        Test that you can submit a GET request to the /users/ path and
            - get a 200 status code.
            - get a response containing a list of users.
        '''
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
        '''
        Test that when you make a get request on the /users/pk/ route
            - that you get a user who already exists in database
            - That hte password of the user is not rendered
        '''
        Users.objects.create(email="simpsons@gmail.com", first_name="Homer",
                             last_name="Simpsons", password="my_password")
        user = Users.objects.get(email="simpsons@gmail.com")
        get_user_response = self.client.get(
            "/api/v1/users/{}/".format(user.id))
        self.assertEqual(get_user_response.status_code, 200)
        self.assertIn(user.first_name,
                      get_user_response.content.decode("utf-8"))
        self.assertIn(user.last_name,
                      get_user_response.content.decode("utf-8"))
        self.assertIn(user.email, get_user_response.content.decode("utf-8"))
        self.assertNotIn("my_password", get_user_response.content.decode("utf-8"))

    def test_not_found_message_for_inexistent_user(self):
        '''
        Test that when you make a get request on the /users/pk/ route for a
        user that does not exist
            - that you get a 404 status code
        '''
        get_user_response = self.client.get(
            "/api/v1/users/{}/".format(1234567))
        self.assertEqual(get_user_response.status_code, 404)
        self.assertIn("Not found.", get_user_response.content.decode("utf-8"))
