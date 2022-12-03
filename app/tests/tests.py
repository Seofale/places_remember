import json
import unittest

from flask import Flask, Response
from flask_login import login_user
from flask_testing import TestCase

from app.core.models import db, lm, User, Place
from app.core.routers import bp


class PlaceTests(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.secret_key = 'secret key'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.register_blueprint(bp)
        db.init_app(app)
        lm.init_app(app)

        @app.route('/auto_login')
        def auto_login():
            user = (User.query.filter_by(fullname='Test User').first())
            login_user(user, remember=True)
            return Response(status=200)

        return app

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            self.populate_db()

        self.login_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def populate_db(self):
        test_user = User(social_id='123', fullname='Test User', photo='test_url')
        test_place1 = Place(
            address='test address 1',
            title='test title 1',
            comment='test comment 1',
            user=test_user
        )
        db.session.add(test_user)
        db.session.add(test_place1)
        db.session.commit()

    def login_client(self):
        self.client.get('/auto_login')

    def test_place_create(self):
        test_data_place = {
            'address': 'test address',
            'title': 'test title',
            'comment': 'test comment'
        }
        self.client.post(
            '/save-place',
            data=json.dumps(test_data_place),
            content_type='application/json',
        )

        self.assertTrue(Place.query.filter_by(title='test title').first() is not None)

    def test_places_list_index_page(self):
        response = self.client.get('/')

        self.assertIn(b'test title 1', response.data)
        self.assertIn(b'test address 1', response.data)
        self.assertIn(b'test comment 1', response.data)


if __name__ == '__main__':
    unittest.main()
