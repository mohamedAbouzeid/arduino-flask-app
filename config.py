import os
basedir = os.path.abspath(os.path.dirname(__file__))

try:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
except KeyError:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

try:
    MEMCACHEDCLOUD_SERVER = os.environ['MEMCACHEDCLOUD_SERVERS']
except KeyError:
    MEMCACHEDCLOUD_SERVER = '127.0.0.1:11211'

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')