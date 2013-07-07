import unittest
import pytest
from paige import *

class TestFunctionalGetRequests(unittest.TestCase):
    def test_home_page(self):
        check = self.app.get('/')
        assert check == 202

    