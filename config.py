import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'project2.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# class TestingConfig(Config):
#     ENV = 'testing'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'tests/test.db')
class Test_Config(Config):
    # TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'tests/testing.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
