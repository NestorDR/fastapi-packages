# -*- coding: utf-8 -*-

# --- Third Party Libraries ---
# sqlalchemy: SQL and ORM toolkit for accessing relational databases.
from sqlalchemy import create_engine

# --- Python modules ---
# os: module which allows access to functionalities dependent on the Operating System.
from os import environ
# urllib: module that collects several modules for working with URLs.
from urllib import parse

# Configure PostgreSQL Database Connection String
host_server = environ.get('POSTGRESQL_SERVER', 'localhost')
db_server_port = parse.quote_plus(str(environ.get('POSTGRESQL_SERVER_PORT', '5432')))
database_name = environ.get('POSTGRESQL_DATABASE_NAME', 'packages')
db_username = parse.quote_plus(str(environ.get('POSTGRESQL_USERNAME', 'postgres')))
db_password = parse.quote_plus(str(environ.get('POSTGRESQL_PASSWORD', 'password')))
ssl_mode = parse.quote_plus(str(environ.get('POSTGRESQL_SSL_MODE', 'prefer')))
DATABASE_URL = \
    f'postgresql://{db_username}:{db_password}@{host_server}:{db_server_port}/{database_name}?sslmode={ssl_mode}'


# Create Engine for PostgreSQL Server.
engine = create_engine(
    DATABASE_URL, pool_size=3, max_overflow=0
)
