# -*- coding: utf-8 -*-

# --- Third Party Libraries ---
# databases: gives you simple asyncio (asynchronous I/O) support for some databases.
from databases import Database
# fastapi: modern, fast (high-performance), web framework for building APIs.
from fastapi import HTTPException, status

# --- Python modules ---
# typing: module which provides runtime support for type hints.
import typing

# --- App modules ---
from app.constants import CREATED, DOWNLOADED, ACTIVATED
# models: contains SQL database model
from app.models import DbModel
# schemas: contains app data schema
from app.schemas import PackageCreate, PackageUpdate


class CRUDPackage:
    """
    CRUD associated with the Package table
    """
    def __init__(self,
                 db_model: DbModel,
                 database: Database):
        """
        Class constructor
        :param db_model: database model
        :param database: database connection
        """
        self.db_model = db_model
        self.database = database

    # Double Underscore (Name Mangling) is used to give classes an easy way to define “private” variables and methods
    @staticmethod
    def __packages_join_statuses_raw_sql() -> str:
        # join tables to obtain status.name, it is necessary to complete the object to be returned by the API
        return 'SELECT packages.id, packages.name, packages.version, statuses.name AS status' \
               ' FROM packages INNER JOIN statuses ON statuses.id = packages.status_id'

    async def create(self,
                     payload: PackageCreate) -> typing.Optional[typing.Mapping]:
        """
        Create a new package
        :param payload: data to create new package
        :return:
        """
        # Validate data content
        name = payload.name.strip()
        if len(name) <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid name.'
            )
        version = payload.version.strip()
        if len(version) <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid version.'
            )
        # Insert
        packages = self.db_model.packages
        query = packages.insert().values(name=name, version=version, status_id=CREATED)
        last_record_id = await self.database.execute(query)
        return {**payload.dict(), 'id': last_record_id, 'status': 'Created'}

    async def fetch_all(self,
                        skip: int,
                        take: int) -> typing.List[typing.Mapping]:
        """
        Get packages list
        :param skip: indicates the number of rows to skip before starting to return the rows
        :param take: determines the number of rows to return/take for the query
        :return: Package list
        """
        query = f'{self.__packages_join_statuses_raw_sql()} LIMIT {take} OFFSET {skip}'
        return await self.database.fetch_all(query)

    async def fetch_one(self,
                        package_id: int) -> typing.Optional[typing.Mapping]:
        """
        Get a package
        :param package_id: identifier of the package to take
        :return: Package read
        """
        query = f'{self.__packages_join_statuses_raw_sql()} WHERE packages.id = :package_id'
        return await self.database.fetch_one(query=query, values=dict(package_id=package_id))
        # Alternatively, if there are no results don't return null and raise a HTTPException with status_code 404
        # It will need: from fastapi import HTTPException
        # package = await self.database.fetch_one(query)
        # if not package:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND, detail=f'Package with ID {package_id} not found.'
        #     )
        # return package

    async def evolve_status(self,
                            package_id: int,
                            new_status_id: int) -> typing.Optional[typing.Mapping]:
        """
        Evolves the state of the package after being downloaded or activated
        :param package_id: identifier of the package that evolves its status
        :param new_status_id: status to which it evolves
        :return: Updated package
        """
        # Get package whose state will evolve
        packages = self.db_model.packages
        query = packages.select().where(packages.c.id == package_id)
        package = await self.database.fetch_one(query)

        # If it does not exist, nothing is returned
        if not package:
            return

        # Evaluate correct evolution to Downloaded or Activated
        current_status_id = package["status_id"]
        if current_status_id == CREATED and new_status_id == DOWNLOADED \
                or current_status_id == DOWNLOADED and new_status_id == ACTIVATED:
            # Update status
            query = packages.update().where(packages.c.id == package_id).values(status_id=new_status_id)
            await self.database.execute(query)

        # Whether the status of the package has evolved or not, get its data to return it
        query = f'{self.__packages_join_statuses_raw_sql()} WHERE packages.id = :package_id'
        return await self.database.fetch_one(query=query, values=dict(package_id=package_id))

    async def update(self,
                     package_id: int,
                     payload: PackageUpdate) -> typing.Optional[typing.Mapping]:
        """
        Update a package
        :param package_id: identifier of the package to update
        :param payload: data to update
        :return: Updated package
        """
        # Validate data content
        name = payload.name.strip()
        if len(name) <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid name.'
            )
        version = payload.version.strip()
        if len(version) <= 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid version.'
            )

        # Check that payload.status_id is valid, currently between 1.Created and 3.Active
        status_id = payload.status_id
        statuses = self.db_model.statuses
        query = statuses.select().where(statuses.c.id == status_id)
        new_status = await self.database.fetch_one(query)
        if not new_status:
            # Don't exist the package status received
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Status identifier {status_id} of the package, invalid.'
            )

        # Get package to update
        packages = self.db_model.packages
        query = packages.select().where(packages.c.id == package_id)
        package = await self.database.fetch_one(query)

        # If it does not exist, nothing is returned
        if not package:
            return

        # Update
        packages = self.db_model.packages
        query = packages.update().where(packages.c.id == package_id) \
            .values(name=name, version=version, status_id=status_id)
        await self.database.execute(query)
        return {**payload.dict(), 'id': package_id, 'status': new_status['name']}

    async def delete(self,
                     package_id: int) -> typing.Optional[typing.Mapping]:
        """
        Delete single Package given its identifier
        :param package_id: identifier of the package to delete
        :return:
        """
        packages = self.db_model.packages
        query = packages.delete().where(packages.c.id == package_id)
        await self.database.execute(query)
        return {'message': f'Package with identifier: {package_id} deleted successfully.'}
