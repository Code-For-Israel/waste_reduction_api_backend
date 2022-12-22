import os
import psycopg2

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

    connection = None
    try:
        # In PostgreSQL, default username is 'postgres' and password is 'postgres'.
        # And also there is a default database exist named as 'postgres'.
        # Default host is 'localhost' or '127.0.0.1'
        # And default port is '5432'.
        conn_string = "user=" + DB_USER + " host=" + _db_host + " password=" + DB_PASS + " port='" + str(DB_PORT) + "'"
        connection = psycopg2.connect(conn_string)
        print('Database connected.')

    except:
        print('Database not connected.')

    if connection is not None:
        connection.autocommit = True

        cur = connection.cursor()

        cur.execute("SELECT datname FROM pg_database;")

        list_database = cur.fetchall()

        if (DB_NAME,) in list_database:
            print("'{}' Database already exist".format(DB_NAME))
        else:
            print("'{}' Database not exist.".format(DB_NAME))
            # SQL command to create database
            cur.execute("CREATE DATABASE {};".format(DB_NAME))
            print('{} database is created.'.format(DB_NAME))
            # After all operation is done close the database connection and cursor
            cur.close()
        connection.close()
        print('Done')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{_db_host}:{DB_PORT}/{DB_NAME}'
