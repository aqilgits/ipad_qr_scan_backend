import os
from flask_sqlalchemy import SQLAlchemy
from constant import db_pass

db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = 'mysql://root:'+db_pass+'@localhost/ipadqrscan'

SQLALCHEMY_TRACK_MODIFICATIONS = True