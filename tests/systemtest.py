import unittest, os, time
from app import app, db
from app.models import User, GameResult, GameBank
from selenium import webdriver


basedir = os.path.abspath(os.path.dirname(__file__))
# Set test variables for test admin user
test_admin_username = "admin"
test_admin_password = "123456"

# Set test variables for test user1
test_user1_username = "Tom"
test_user1_password ="jdkfjs"

# Set test variables for test game
test_game1 = "7,6,3,1,9,8,2,5,4,4,9,5,6,7,2,8,3,1,1,2,8,3,5,4,9,6,7,2,4,9,8,6,5,1,7,3,3,5,7,9,2,1,4,8,6,8,1,6,4,3,7,5,2,9,6,8,1,2,4,3,7,9,5,5,3,2,7,1,9,6,4,8,9,7,4,5,8,6,3,1,2"
test_game1_uploadId = '1'


class SystemTest(unittest.TestCase):
    driver = None

    def setUp(self):
        # self.driver = webdriver.Firefox(executable_path=os.path.join(basedir, 'geckodriver'))
        self.driver = webdriver.Firefox(executable_path=os.path.join(basedir, 'geckodriver'))

        if not self.driver:
            self.skipTest('Web browser not available')
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = \
                'sqlite:///' + os.path.join(basedir, 'test.db')
            self.app = app.test_client()  # creates a virtual test environment
            db.create_all()
            # s1 = Student(id='22222222', first_name='Test', surname='Case', cits3403=True)
            # s2 = Student(id='11111111', first_name='Unit', surname='Test', cits3403=True)
            # lab = Lab(lab='test-lab', time='now')
            # db.session.add(s1)
            # db.session.add(s2)
            # db.session.add(lab)
            # db.session.commit()

            # create test admin user
            self.admin = User(username=test_admin_username,
                              password=test_admin_password,
                              user_type=0)
            # create test user
            self.user = User(username=test_user1_username,
                              password=test_user1_password,
                              user_type=1)

            # create test game
            self.game = GameBank(game=test_game1, uploaderId=test_game1_uploadId)
            db.session.add(self.admin)
            db.session.add(self.user)
            db.session.add(self.game)
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


    def test_registion(self):
        self.driver.get('http://localhost:5000/register')
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id("register_username").send_keys('Jija')
        self.driver.find_element_by_id("password-field").send_keys('129378')
        self.driver.find_element_by_id("register_button").click()
        time.sleep(1)
        page = self.driver.current_url
        self.assertEqual(page, 'http://localhost:5000/login')


    def test_login_admin_user(self):
        # login_link = self.get_server_url() + 'login'
        self.driver.get('http://localhost:5000/login')
        self.driver.implicitly_wait(5)
        self.driver.find_element_by_id("login_username").send_keys(test_admin_username)
        self.driver.find_element_by_id("password-field").send_keys(test_admin_password)
        self.driver.find_element_by_id("login_button").click()
        time.sleep(2)
        result = self.driver.find_element_by_id("upload_button").value_of_css_property("display")
        self.assertEqual(result, "inline-block")


    def test_upload(self):
        self.test_login_admin_user()
        time.sleep(1)
        self.driver.find_element_by_id("upload_button").click()
        time.sleep(1)
        self.driver.find_element_by_id("gameString").send_keys("6,9,5,1,2,3,7,4,8,7,4,1,8,6,9,2,5,3,2,3,8,4,5,7,1,6,9,8,1,6,7,4,5,3,9,2,5,2,4,3,9,8,6,7,1,3,7,9,6,1,2,4,8,5,4,8,3,9,7,1,5,2,6,1,6,2,5,8,4,9,3,7,9,5,7,2,3,6,8,1,4")
        time.sleep(1)
        self.driver.find_element_by_id("submit_form").click()
        self.driver.implicitly_wait(5)
        time.sleep(1)
        result = self.driver.find_element_by_id("result")
        self.assertEqual(result.text, 'fail')

if __name__ == '__main__':
    unittest.main(verbosity=2)
    # def test_register(self):
    #     s = Student.query.get('22222222')
    #     self.assertEqual(s.first_name, 'Test', msg='student exists in db')
    #     self.driver.get('http://localhost:5000/register')
    #     self.driver.implicitly_wait(5)
    #     num_field = self.driver.find_element_by_id('student_number')
    #     num_field.send_keys('22222222')
    #     pref_name = self.driver.find_element_by_id('prefered_name')
    #     pref_name.send_keys('Testy')
    #     new_pin = self.driver.find_element_by_id('new_pin')
    #     new_pin.send_keys('0000')
    #     new_pin2 = self.driver.find_element_by_id('new_pin2')
    #     new_pin2.send_keys('0000')
    #     time.sleep(1)
    #     self.driver.implicitly_wait(5)
    #     submit = self.driver.find_element_by_id('submit')
    #     submit.click()
    #     # check login success
    #     self.driver.implicitly_wait(5)
    #     time.sleep(1)
    #     logout = self.driver.find_element_by_partial_link_text('Logout')
    #     self.assertEqual(logout.get_attribute('innerHTML'), 'Logout Testy', msg='Logged in')
