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

    def is_logged_in(self):
        try:
            return self.app.cookie_jar._cookies['localhost.local']['/'][REAL_KEY].value == REAL_VALUE
        except KeyError:
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
class TestAdminPages(BaseClass):
    def test_logged_in(self):   
        self.login()
        response = self.app.get('/admin')
        assert response.status_code == 200

    def test_not_logged_in(self):
        assert not self.is_logged_in()
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

    def test_new_image_page(self):
        self.login()
        response = self.app.get('/new_image')
        assert response.status_code == 200

    def test_delete_image_page(self):
        self.login()
        response = self.app.get('/delete_image')
        assert response.status_code == 200

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
        )
        assert response.status_code == 302
        assert not self.is_logged_in()

    def test_no_credentials(self):
        response = self.app.post('/login/authenticate')
        assert response.status_code == 302
        assert not self.is_logged_in()

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
    def test_logout_logged_in(self):
        #at start you will be logged in
        self.app.set_cookie('localhost', REAL_KEY, REAL_VALUE)
        
        assert self.is_logged_in()
        response = self.app.post('/logout')
        
        #at end you will not be logged in
        assert not self.is_logged_in()

    def test_logout_not_logged_in(self):
        assert not self.is_logged_in()

        response = self.app.post('/logout')
        
        assert not self.is_logged_in()


@pytest.mark.new_image
class TestImageUpload(BaseClass):
    #tests that if form information with no information results in no new image to the website
    def test_no_info(self):
        response = self.app.post('/new_image/upload')
        #if no information posted, should get a 
        assert response.status_code == 302
        


