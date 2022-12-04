import os

with open(os.environ['POSTGRES_USER_FILE']) as f:
    _db_user = f.read()

with open(os.environ['POSTGRES_PASSWORD_FILE']) as f:
    _db_pass = f.read()


class BaseConfig(object):
    #DEBUG = os.environ['DEBUG']
    DB_NAME = "WasteReduction"
    DB_USER = _db_user
    DB_PASS = _db_pass
    DB_PORT = 5432
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@postgres:{DB_PORT}/{DB_NAME}'
