import os

## if running from docker-compose
if "DOCKER" in os.environ:
    ## Loads DB user name from secret file - if you are running locally just add environment variable with that name pointing to a file with the user
    ## for example (on Windows) ==> SET POSTGRES_USER_FILE=c:\temp\secrets\user.txt
    with open(os.environ['POSTGRES_USER_FILE']) as f:
        _db_user = f.read()

    ## Loads DB password name from secret file - if you are running locally just add environment variable with that name pointing to a file with the password
    ## for example (on Windows) ==> SET POSTGRES_PASSWORD_FILE=c:\temp\secrets\password.txt
    with open(os.environ['POSTGRES_PASSWORD_FILE']) as f:
        _db_pass = f.read()
    _db_host = 'postgres' ## as the service name in the docker-compose yaml

else:
    _db_user = 'postgres'
    _db_pass = 'data1'
    _db_host = 'localhost'

## Building the DB connection string
class BaseConfig(object):
    DB_NAME = "waste_reduction"
    DB_USER = _db_user
    DB_PASS = _db_pass
    DB_PORT = 5432
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{_db_host}:{DB_PORT}/{DB_NAME}'
