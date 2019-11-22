import os
DEBUG = True
SECRET_KEY = os.urandom(24)
HOST = '127.0.0.1'
USERNAME = 'root'
PASSWORD = '123456'
DATABASE = 'app_project_demo'
PORT = '3306'
DRIVER = 'pymysql'
SQL = 'mysql'
DB_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(SQL,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False