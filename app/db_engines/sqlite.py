# -*- coding: utf-8 -*-

# --- Third Party Libraries ---
# sqlalchemy: SQL and ORM toolkit for accessing relational databases.
import sqlalchemy

# Configure SQLite Database Connection String
DATABASE_URL = "sqlite:///packages.db"

# Create Engine for SQLite Server.
engine = sqlalchemy.create_engine(
    DATABASE_URL,
    # Required for SQLite.
    connect_args={"check_same_thread": False}
)
