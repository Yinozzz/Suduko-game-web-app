import unittest, os, time
from app import app, db
from app.models import User, GameResult, GameBank
from selenium import webdriver
from datetime import date


basedir = os.path.abspath(os.path.dirname(__file__))


# Set test variables for test game
test_game1 = "7,6,3,1,9,8,2,5,4,4,9,5,6,7,2,8,3,1,1,2,8,3,5,4,9,6,7,2,4,9,8,6,5,1,7,3,3,5,7,9,2,1,4,8,6,8,1,6,4,3,7,5,2,9,6,8,1,2,4,3,7,9,5,5,3,2,7,1,9,6,4,8,9,7,4,5,8,6,3,1,2"


class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        # self.driver = webdriver.Firefox(executable_path=os.path.join(basedir, 'geckodriver'))
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir, 'geckodriver'))
        if not self.driver:
            self.skipTest('Web browser not available')
        else:
            db.init_app(app)
            db.create_all()
            game = GameBank(uploaderId=1, game=test_game1, upload_time=date.fromtimestamp(time.time()), current_game='1')
            db.session.add(game)
            db.session.commit()

            self.driver.maximize_window()
            self.driver.get('http://localhost:5000/')

    def tearDown(self):
        if self.driver:
            self.driver.close()
            db.session.query(User).delete()
            db.session.query(GameResult).delete()
            db.session.query(GameBank).delete()
            db.session.commit()
            db.session.remove()


    def test_registion_login(self):
        self.driver.get('http://localhost:5000/register')
        self.driver.implicitly_wait(5)
        self.driver.find_element("id", "register_username").send_keys('Jija')
        self.driver.find_element("id", "password-field").send_keys('129378')
        self.driver.find_element("id", "register_button").click()
        time.sleep(1)
        page = self.driver.current_url
        self.assertEqual(page, 'http://localhost:5000/login', msg="Successful registion")

        self.driver.find_element("id", "login_username").send_keys('Jija')
        self.driver.find_element("id", "password-field").send_keys('129378')
        self.driver.find_element("id","login_button").click()
        time.sleep(2)

        result = self.driver.find_element("id", "logout")
        self.assertEqual(result.get_attribute('innerHTML'), "logout", msg="Successful login")



if __name__ == '__main__':
    unittest.main()