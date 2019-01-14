import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ashiri-agba'
    GOOGLE_OAUTH_CLIENT_ID = \
        os.environ.get('GOOGLE_OAUTH_CLIENT_ID') or \
        '1031325655763-7ls7vqathu75llccmqvsrg1' \
        'jc5ugt2e7.apps.googleusercontent.com'
    GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET') \
        or 'AO0PkP4OzA4tsVl8ElH9Irsy'
    SCOPE = ["https://www.googleapis.com/auth/plus.me",
             "https://www.googleapis.com/auth/userinfo.email"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_ADDRESS = os.environ.get('API_ADDRESS') or 'http://localhost:8001'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    EXPLAIN_TEMPLATE_LOADING = True
    DATABASE = os.environ.get('DATABASE') or 'catalog'
    INDEX_TEMPLATE = 'catalogapp/index.html'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = os.environ.get(
        'OAUTHLIB_INSECURE_TRANSPORT') or '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = os.environ.get(
        'OAUTHLIB_RELAX_TOKEN_SCOPE') or '1'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or \
        'postgresql+psycopg2:///' + DATABASE


class TestingConfig(BaseConfig):
    DEBUG = True
    DATABASE = 'catalog'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
        'postgresql+psycopg2://vagrant:vagrant@localhost/' + DATABASE


class ProductionConfig(BaseConfig):
    DEBUG = False
    DATABASE = 'catalog'
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or \
        'postgresql+psycopg2://vagrant:vagrant@localhost/' + DATABASE
