import unittest
import pytest
import requests
from paige import *

class TestFunctionalGetRequests(unittest.TestCase):
    def test_home_page(self):
        check = requests.get('/')
        assert check.status_code == 202

