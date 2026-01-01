# config.py
import os

class Configuration:
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/db_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
