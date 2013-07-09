import unittest
import pytest
import flask
from paige import app

class BaseClass(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

class TestFunctionalGetRequests(BaseClass):
    def test_home_page(self):
        response = self.app.get('/')
        assert response.status_code == 200

@pytest.mark.admin
class TestAdminPage(BaseClass):
    @pytest.mark.x
    def test_logged_in(self):   
        self.app.set_cookie('localhost', '9f4yZIjq', 'CsyGlIE0')
        assert self.app.cookie_jar._cookies
        response = self.app.get('/admin')
        assert response.status_code == 200

    @pytest.mark.y
    def test_not_logged_in(self):
        assert not self.app.cookie_jar._cookies
        response = self.app.get('/admin')
        assert response.status_code == 401
