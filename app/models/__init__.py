# -*- coding: utf-8 -*-

# --- Third Party Libraries ---
# sqlalchemy: SQL and ORM toolkit for accessing relational databases.
from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, String

# --- App modules ---
from .packages import Packages
from .statuses import Statuses


class DbModel:
    """
    Create SQL Alchemy model via imperative mapping, construct the tables directly.
    Since databases library uses queries build using SQLAlchemy core, then you'll need
     to declare/use the tables in code.
    Visit: https://github.com/encode/databases/blob/master/docs/database_queries.md
           https://docs.sqlalchemy.org/en/14/core/index.html
    """
    def __init__(self,
                 metadata: MetaData):
        """
        Class constructor
        :param metadata: SQL Alchemy MetaData object that will hold the tables
        """
        self.metadata = metadata

        # Table representations
        self.packages = Packages(self.metadata).table
        self.statuses = Statuses(self.metadata).table
