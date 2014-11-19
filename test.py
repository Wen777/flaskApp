# -*- coding: utf-8 -*-
from app import app
import unittest

class FlaskTestCase(unittest.TestCase):

    # Ensure that flask was set up correctly

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that login page loads correctly

    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'Please login' in response.data)

    # Ensure that login behaves correctly given the correct credentials

    def test_login_correct(self):
        tester = app.test_client(self)
        response = tester.post("/login",
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn( b'You are just logged in', response.data )

    # Ensure that login behaves correctly given the incorrect credentials

    def test_login_incorrect(self):
        tester = app.test_client(self)
        response = tester.post("/login",
            data=dict(username="wrong", password="admin"),
            follow_redirects=True
        )
        self.assertIn( b'Invalid Credentials. Please try again.', response.data )

    # Ensure that logout behaves correctly

    def test_logout(self):
        tester = app.test_client(self)
        tester.post("/login",
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        response = tester.get("/logout", follow_redirects=True)
        self.assertIn( b'You are just logged out', response.data )

    # Ensure main page login
    def test_main_route_require_login(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text', follow_redirects=True)
        self.assertTrue(b'You need to login first' in response.data)

    # Ensure that posts show up on the page
    def test_post_show_up(self):
        tester = app.test_client(self)
        response = tester.post("/login",
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn( b'Hello from shell', response.data )

if __name__ == "__main__":
    unittest.main()

