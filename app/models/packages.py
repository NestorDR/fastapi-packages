# -*- coding: utf-8 -*-

# --- Third Party Libraries ---
# sqlalchemy: SQL and ORM toolkit for accessing relational databases.
from sqlalchemy import MetaData, Table, Column, ForeignKey, Integer, String


class Packages:
    """
    Table representation Packages
    """
    def __init__(self,
                 metadata: MetaData):
        """
        Class constructor
        :param metadata: SQL Alchemy MetaData object that will hold the tables
        """
        self.metadata = metadata

        # table representation Packages
        self.table = Table(
            'packages',
            self.metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(length=200), nullable=False),
            Column('version', String(length=50), nullable=False),
            Column('status_id', Integer, ForeignKey("statuses.id"), nullable=False),
        )
