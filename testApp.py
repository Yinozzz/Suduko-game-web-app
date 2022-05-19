import json
import unittest
import time
from datetime import date

from werkzeug.security import generate_password_hash

from app import app, db
from config import Test_Config_Unit
from app.models import GameResult, User, GameBank


class TestAPP(unittest.TestCase):
    def setUp(self):
        # app.config.from_object(Test_Config_Unit)
        self.app = app
        self.client = self.app.test_client()
        db.create_all()
        default1 = '6,9,5,1,2,3,7,4,8,7,4,1,8,6,9,2,5,3,2,3,8,4,5,7,1,6,9,8,1' \
                   ',6,7,4,5,3,9,2,5,2,4,3,9,8,6,7,1,3,7,9,6,1,2,4,' \
                   '8,5,4,8,3,9,7,1,5,2,6,1,6,2,5,8,4,9,3,7,9,5,7,2,3,6,8,1,4'
        if User.query.filter(User.username == 'admin').first() is None:
            admin = User(username='admin', password=generate_password_hash('123456'), user_type=0,
                         head_pic_url='./static/default_head_pic.jpg')
            db.session.add(admin)
            db.session.commit()
        if User.query.filter(User.username == 'new').first() is None:
            new = User(username='new', password=generate_password_hash('123456'), user_type=0,
                         head_pic_url='./static/default_head_pic.jpg')
            db.session.add(new)
            db.session.commit()
        if GameBank.query.filter(GameBank.game == default1).first() is None:
            default_game = GameBank(uploaderId=1, game=default1,
                                    upload_time=date.fromtimestamp(time.time()), current_game='1')
            db.session.add(default_game)
            db.session.commit()
        if GameResult.query.filter(GameResult.id == 1).first() is None:
            default_result = GameResult(playerId=1 , start_time=date.fromtimestamp(time.time()), finish_time=date.fromtimestamp(time.time()), time_spent=10)
            db.session.add(default_result)
            db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_config(self):
        self.assertEqual(self.app.config['TESTING'], True)
        self.assertIsNotNone(self.app.config['SQLALCHEMY_DATABASE_URI'])

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_introduction(self):
        response = self.client.get('/introduction')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response_get = self.client.get('/register')
        self.assertEqual(response_get.status_code, 200)
        params = dict()
        params['username'] = 'li'
        params['password'] = '123456'
        response_post_normal = self.client.post('/register', data=params, follow_redirects=True)
        self.assertEqual(response_post_normal.status_code, 200)

    def test_login(self):
        response_get = self.client.get('/login')
        self.assertEqual(response_get.status_code, 200)
        params = dict()
        params['username'] = 'admin'
        params['password'] = '123456'
        response_post_normal = self.client.post('/login', data=params, follow_redirects=True)
        self.assertEqual(response_post_normal.status_code, 200)

    def test_game_get(self):
        self.client.get('/')
        response_get = self.client.get('/game')
        self.assertEqual(response_get.status_code, 200)

    def test_game_post(self):
        params_login = dict()
        params_login['username'] = 'admin'
        params_login['password'] = '123456'
        self.client.post('/login', data=params_login, follow_redirects=True)

        params = dict()
        params["start_time"] = 1652882890158
        params["finish_time"] = 1652882884913
        params[
            "game_string"] = "6,9,5,1,2,3,7,4,8,7,4,1,8,6,9,2,5,3,2,3,8,4,5,7,1,6,9,8,1,6,7,4,5,3,9,2,5,2,4,3,9,8,6,7,1,3,7,9,6,1,2,4,8,5,4,8,3,9,7,1,5,2,6,1,6,2,5,8,4,9,3,7,9,5,7,2,3,6,8,1,4"
        params_json = json.dumps(params)
        response_post_normal = self.client.post('/game', content_type='application/json', data=params_json)
        self.assertEqual(json.loads(response_post_normal.text).get('game_result'), 'success')
        print(response_post_normal)

    def test_game_post2(self):
        params_login = dict()
        params_login['username'] = 'admin'
        params_login['password'] = '123456'
        self.client.post('/login', data=params_login, follow_redirects=True)

        params = dict()
        params["start_time"] = 1652882890158
        params["finish_time"] = 1652882884913
        params[
            "game_string"] = "6,9,9,1,2,3,7,4,8,7,4,1,8,6,9,2,5,3,2,3,8,4,5,7,1,6,9,8,1,6,7,4,5,3,9,2,5,2,4,3,9,8,6,7,1,3,7,9,6,1,2,4,8,5,4,8,3,9,7,1,5,2,6,1,6,2,5,8,4,9,3,7,9,5,7,2,3,6,8,1,4"
        params_json = json.dumps(params)
        response_post_normal = self.client.post('/game', content_type='application/json', data=params_json)
        self.assertEqual(json.loads(response_post_normal.text).get('game_result'), 'fail')

    def test_upload_get(self):
        params = dict()
        params['username'] = 'admin'
        params['password'] = '123456'
        self.client.post('/login', data=params, follow_redirects=True)
        response_get = self.client.get('/upload')
        self.assertEqual(response_get.status_code, 200)

    def test_upload_post(self):
        params = dict()
        params['username'] = 'admin'
        params['password'] = '123456'
        self.client.post('/login', data=params, follow_redirects=True)

        params_game = dict()
        params_game["game_string"] = "6,9,5,1,2,3,7,4,8,7,4,1,8,6,9,2,5,3,2,3,8,4,5,7,1,6,9,8,1,6,7,4,5,3,9,2,5,2,4,3,9,8,6,7,1,3,7,9,6,1,2,4,8,5,4,8,3,9,7,1,5,2,6,1,6,2,5,8,4,9,3,7,9,5,7,2,3,6,8,1,4"
        params_game_json = json.dumps(params_game)
        response_post_normal = self.client.post('/upload', content_type='application/json', data=params_game_json)
        self.assertEqual(response_post_normal.text, 'the game already exits')

    def test_upload_post2(self):
        params = dict()
        params['username'] = 'admin'
        params['password'] = '123456'
        self.client.post('/login', data=params, follow_redirects=True)

        params_game = dict()
        params_game[
            "game_string"] = "'7,4,9,5,2,3,8,1,6,5,2,3,1,6,8,4,9,7,8,6,1,9,4,7,5,3,2,6,7,2,4,1,9,3,8,5,4,9,5,8,3,6,7,2,1,1,3,8,2,7,5,9,6,4,3,8,6,7,5,2,1,4,9,9,5,4,6,8,1,2,7,3,2,1,7,3,9,4,6,5,8'"
        params_game_json = json.dumps(params_game)
        response_post_normal = self.client.post('/upload', content_type='application/json', data=params_game_json)
        self.assertEqual(response_post_normal.text, 'success')

    def test_upload_post3(self):
        params = dict()
        params['username'] = 'admin'
        params['password'] = '123456'
        self.client.post('/login', data=params, follow_redirects=True)

        params_game = dict()
        params_game[
            "game_string"] = "'7,4,4,5,2,3,8,1,6,5,2,3,1,6,8,4,9,7,8,6,1,9,4,7,5,3,2,6,7,2,4,1,9,3,8,5,4,9,5,8,3,6,7,2,1,1,3,8,2,7,5,9,6,4,3,8,6,7,5,2,1,4,9,9,5,4,6,8,1,2,7,3,2,1,7,3,9,4,6,5,8'"
        params_game_json = json.dumps(params_game)
        response_post_normal = self.client.post('/upload', content_type='application/json', data=params_game_json)
        self.assertEqual(response_post_normal.text, 'fail')

    def test_personal_get(self):
        params = dict()
        params['username'] = 'admin'
        params['password'] = '123456'
        self.client.post('/login', data=params, follow_redirects=True)

        response_post_normal = self.client.get('/personal')
        self.assertEqual(response_post_normal.status_code, 200)

    def test_personal_get2(self):
        response_post_normal = self.client.get('/personal')
        self.assertEqual(response_post_normal.status_code, 302)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAPP)
    unittest.TextTestRunner(verbosity=2).run(suite)
