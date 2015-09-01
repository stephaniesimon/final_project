import os
import unittest

from server import app, session

from model import db, User, Question
import seed
from sqlalchemy import exc


class TestCase (unittest.TestCase):
    def setUp(self):
        """Set up a testing db"""

        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()

        db.app = app
        db.init_app(app)
        db.create_all()

    def tearDown(self):
        """Delete testing db"""

        db.session.remove()
        db.drop_all()

    # ==============================================================================
    # Testing User Model
    # ==============================================================================

    def test_user(self):

        u = User(first_name='John', email='jsmith@example.com', password='test') # Make a user
        db.session.add(u)
        db.session.commit()
        self.assertEqual(u.first_name, 'John')

        # Duplicate critical information
        u = User(first_name='Jane', email='jsmith@example.com', password='test')
        db.session.add(u)
        with self.assertRaises(exc.IntegrityError):
            db.session.commit()
        db.session.rollback()

        # See what happens if we are missing information
        u = User(first_name='Jane', email='jsmith@example.com')
        db.session.add(u)
        with self.assertRaises(exc.IntegrityError):
            db.session.commit()
        db.session.rollback()

# ==============================================================================
# Testing Login/Logout Views
# ==============================================================================

    def login(self, email, password):
        return self.app.post('/login', data=dict(
                                    email=email,
                                    password=password
                                    ), follow_redirects=True)

    def logout(self):

        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):

        q = Question(question_text="Why?")
        db.session.add(q)
        db.session.commit()

        u = User(first_name='John', email='jsmith@example.com', password='test')
        db.session.add(u)
        db.session.commit()

        # rv = response from server of the profile page (hopefully!)
        rv = self.login('jsmith@example.com', 'test')
        # self.assertTrue(session['user_id'] == u.user_id)
        self.assertTrue('Logout' in rv.data)
        self.assertFalse('Log In' in rv.data)

        rv = self.logout()
        # self.assertTrue('user_id' not in session)
        self.assertTrue('login' in rv.data)

        rv = self.login('jsmith@example.com', 'testb')
        self.assertTrue('User name and password do not match' in rv.data)

        rv = self.login('jsmith2@example.com', 'test')
        self.assertTrue('This email is not registered - please create an account' in rv.data) 



if __name__ == '__main__':
    unittest.main()
