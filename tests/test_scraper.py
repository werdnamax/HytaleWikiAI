import unittest
import requests

class TestSoupWeb(unittest.TestCase):

    def test_web(self):
        response = requests.get('https://www.google.com/')
        self.assertEqual(response.status_code, 200)

