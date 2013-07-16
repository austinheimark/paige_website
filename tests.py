import unittest
import pytest
import flask
from paige import app
import paige

class BaseClass(unittest.TestCase):
    def setUp(self):
        paige.app.config['TESTING'] = True
        self.app = app.test_client()

class TestFunctionalGetRequests(BaseClass):
    def test_home_page(self):
        response = self.app.get('/')
        assert response.status_code == 200

@pytest.mark.admin
class TestAdminPage(BaseClass):
    def test_logged_in(self):   
        self.app.set_cookie('localhost', '9f4yZIjq', 'CsyGlIE0')
        response = self.app.get('/admin')
        assert response.status_code == 200

    def test_not_logged_in(self):
        assert not self.app.cookie_jar._cookies
        response = self.app.get('/admin')
        assert response.status_code == 401

    def test_cheater_cookie(self):
        self.app.set_cookie('localhost', 'cheater-key', 'cheater-value')
        response = self.app.get('/admin')
        assert response.status_code == 401

    def test_cheater_value_cookie(self):
        self.app.set_cookie('localhost', '9f4yZIjq', 'cheater-value')
        response = self.app.get('/admin')
        assert response.status_code == 401

    def test_cheater_key_cookie(self):
        self.app.set_cookie('localhost', 'cheater-key', 'CsyGlIE0')
        response = self.app.get('/admin')
        assert response.status_code == 401