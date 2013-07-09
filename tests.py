import unittest
import pytest
from paige import app

class TestFunctionalGetRequests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        assert response.status_code == 200

@pytest.mark.admin
class TestAdminPage(unittest.TestCase):
    def test_admin_page(self):
        response = self.app.get('/admin')        
        assert response.status_code == 200


    # this tests to make sure that you can open up the admin
    # page only if you are logged in. Otherwise you cannot
    def test_admin_page_login(self):
        # need to log in the administrator
        # see that they can access the admin page and no one else can
        response = self.app.get('/admin')
        assert response.status_code == 401
