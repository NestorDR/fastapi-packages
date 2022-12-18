# -*- coding: utf-8 -*-

# --- Third Party Libraries ---
# sqlalchemy: SQL and ORM toolkit for accessing relational databases.
from sqlalchemy import MetaData, Table, Column, Integer, String


class Statuses():
    """
    Table representation Statuses
    """
    def __init__(self, metadata: MetaData, *args, **kw):
        """
        Class constructor
        :param metadata: SQL Alchemy MetaData object that will hold the tables
        """
        # Call constructor of SQLAlchemy Table superclass
        super().__init__(*args, **kw)

        self.metadata = metadata

        # table representation Statuses
        self.table = Table(
            'statuses',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(length=20), nullable=False),
        )
