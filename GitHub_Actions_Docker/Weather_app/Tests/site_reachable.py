import unittest
import requests

url = "http://127.0.0.1:8000"

class TestSiteReachable(unittest.TestCase):
    def setUp(self):
        self.response = requests.get(url)
    
    def test_url_ok(self):
        self.assertEqual(self.response.status_code, 200, "Site is reachable")

   
######################################################
    

if __name__ == '__main__': 
     unittest.main()