import unittest
import pytest
import requests
from paige import app

class TestFunctionalGetRequests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @pytest.mark.a
    def test_home_page(self):
        response = self.app.get('/')
        assert response.status_code == 200

