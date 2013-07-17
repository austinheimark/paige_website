import unittest
import pytest
import flask
from paige import (
    app,
    REAL_KEY,
    REAL_VALUE,
    VALID_PASSWORD,

    )
import paige

INCORRECT_RESPONSE = 'incorrect'

class BaseClass(unittest.TestCase):
    def setUp(self):
        paige.app.config['TESTING'] = True
        self.app = app.test_client()

    def is_not_logged_in(self):
        if not self.app.cookie_jar._cookies:
            return True
        else:
            return False

    def login(self):
        self.app.set_cookie('localhost', REAL_KEY, REAL_VALUE)


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
        self.login()
        response = self.app.get('/admin')
        assert response.status_code == 200

    def test_not_logged_in(self):
        assert self.is_not_logged_in()
        response = self.app.get('/admin')
        assert response.status_code == 401

    def test_cheater_cookie(self):
        self.app.set_cookie('localhost', INCORRECT_RESPONSE, INCORRECT_RESPONSE)
        response = self.app.get('/admin')
        assert response.status_code == 401

    def test_cheater_value_cookie(self):
        self.app.set_cookie('localhost', REAL_KEY, INCORRECT_RESPONSE)
        response = self.app.get('/admin')
        assert response.status_code == 401

    def test_cheater_key_cookie(self):
        self.app.set_cookie('localhost', INCORRECT_RESPONSE, REAL_VALUE)
        response = self.app.get('/admin')
        assert response.status_code == 401

@pytest.mark.login
class TestLogin(BaseClass):
    def test_page(self):
        response = self.app.get('/login')
        assert response.status_code == 200

    def test_bad_credentials(self):
        response = self.app.post(
            '/login/authenticate', 
            data={
                'password':'incorrect'
            }

    def test_no_credentials(self):
        response = self.app.post('/login/authenticate')
        assert response.status_code == 401
        assert self.is_not_logged_in()

    def test_valid_credentials(self):
        response = self.app.post(
            '/login/authenticate',
            data={
                'password':VALID_PASSWORD
                },
            follow_redirects=True
            )
        assert response.status_code == 200

@pytest.mark.logout
class TestLogout(BaseClass):
    def test_logout_when_logged_in(self):
        #at start you will be logged in
        self.login()

        #then get the response from the logout function, which will clear the cookies
        response = self.app.post('/logout')
        
        #at end you will not be logged in (logged out) because the cookies will no longer be present
        assert self.is_not_logged_in()

    @pytest.mark.a
    def test_logout_not_logged_in(self):
        #make sure not logged in
        assert self.is_not_logged_in

        response = self.app.post('/logout')

        #should still not be logged in
        assert self.is_not_logged_in



