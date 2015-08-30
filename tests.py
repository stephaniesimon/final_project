import os
import unittest

from server import app
from model import db, User
import seed
from sqlalchemy import exc


class TestCase (unittest.TestCase):
	def setUp(self):
		"""Set up a testing db"""

		self.app = app.test_client()
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
		db.app = app
		db.initi_app(app)
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

        u = User(first_name='John', email='jsmith@example.com', password='test')
        db.session.add(u)
        db.session.commit()

        rv = self.login('jsmith@example.com', 'test')
        self.assertTrue('Logout' in rv.data)

        rv = self.logout()
        self.assertTrue('Log In' in rv.data)

        rv = self.login('jsmith@example.com', 'testb')
        self.assertTrue('User name and password do not match' in rv.data)

        rv = self.login('jsmith2@example.com', 'test')
        self.assertTrue('This email is not registered - please create an account' in rv.data) 



if __name__ == '__main__':
    unittest.main()
