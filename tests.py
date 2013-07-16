import unittest
import pytest
import flask
from paige import app
import paige

class BaseClass(unittest.TestCase):
    def setUp(self):
        paige.app.config['TESTING'] = True
        self.app = app.test_client()

@pytest.mark.validpages
class TestFunctionalGetRequests(BaseClass):
    def test_home_page(self):
        response = self.app.get('/')
        assert response.status_code == 200

    def test_contact_page(self):
        response = self.app.get('/contact')
        assert response.status_code == 200

    def test_drawings_page(self):
        response = self.app.get('/drawings')
        assert response.status_code == 200

    def test_resume_page(self):
        response = self.app.get('/resume')
        assert response.status_code == 200

    def test_paintings_page(self):
        response = self.app.get('/paintings')
        assert response.status_code == 200

    def test_sculptures_page(self):
        response = self.app.get('/sculptures')
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

@pytest.mark.login
class TestLogin(BaseClass):
    def test_login_page(self):
        response = self.app.get('/login')
        assert response.status_code == 200

    def test_login_bad_credentials(self):
        self.app.set_cookie('localhost', 'cheater-key', 'cheater-value')
        response = self.app.get('/login/authenticate')
        assert response.status_code == 401







