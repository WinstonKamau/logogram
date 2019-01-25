'''Test the common root for the project '''
from logogram_v1.tests.base_test import BaseTestCase


class RootView(BaseTestCase):

    def setUp(self):
        super(RootView, self).setUp()

    def test_get_request_on_root_view(self):
        '''
        Test that when you send a get request to the root view:
            - That you get a welcome message
        '''
        root_view_response = self.client.get("/api/v1/")
        root_view_message = "Welcome to the Logogram Application."
        self.assertContains(root_view_response, root_view_message)

    def test_get_view(self):
        '''
        Test that when you send a post request to the root view:
            - That you get a 405 Method Not allowed as the view is only for
            GET requests
        '''
        root_view_response = self.client.post("/api/v1/")
        self.assertEqual(root_view_response.status_code, 405)
