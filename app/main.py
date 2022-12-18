# -*- coding: utf-8 -*-

# --- Third Party Libraries ---
# databases: gives you simple asyncio (asynchronous I/O) support for some databases.
#            It supports either raw SQL or queries build using SQLAlchemy Core.
#            It's suitable for integrating against any async Web framework, such as FastAPI.
#            Visit https://www.encode.io/databases/
from databases import Database
# fastapi: modern, fast (high-performance), web framework for building APIs.
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# fastapi-simple-security: library which provides API key based security.
from fastapi_simple_security import api_key_router, api_key_security
# sqlalchemy: SQL and ORM toolkit for accessing relational databases.
from sqlalchemy import MetaData
# urllib: module that collects several modules for working with URLs.
from urllib import parse

# --- Python modules ---
# os: module which allows access to functionalities dependent on the Operating System.
from os import environ
# typing: module which provides runtime support for type hints.
from typing import List

# --- App modules ---
# constants: contains constants data
from .constants import DOWNLOADED, ACTIVATED
# models: contains SQL database model
from .models import DbModel
# schemas: contains app data schema
from .schemas import PackageCreate, PackageUpdate, Package
# db_engines: contains the database engine to use, you can choose SQLite or PostgreSQL
from .db_engines import sqlite, postgresql

from .crud import CRUDPackage

# Create application using FastAPI
app = FastAPI(title='Packages REST API using FastAPI Async EndPoints')

# Create a SQL Alchemy model that will support the features of the db_engines.
metadata = MetaData()
db_model = DbModel(metadata)

# Select SQL Engine, default SQLite
selected_db_engine = parse.quote_plus(str(environ.get('FASTAPI_PACKAGES_DB_ENGINE', 'sqlite')).lower())
if selected_db_engine == 'sqlite':
    engine = sqlite.engine
    database_url = sqlite.DATABASE_URL
elif selected_db_engine == 'postgresql':
    engine = postgresql.engine
    database_url = postgresql.DATABASE_URL
else:
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="DB engine error")

# Create tables in db_engines, if they don't exist
metadata.create_all(engine)

# Create database instance through which the API will access the stored data
database = Database(database_url)

# Add CORS enabling it at the app level by allowing requests from all origins via allow_origins=[*].
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Add API key based security from fastapi_simple_security
app.include_router(api_key_router, prefix="/auth", tags=["_auth"])


# Add application Startup & Shutdown events
@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


# Create API Routes

# API Key validation test
@app.get("/secure", dependencies=[Depends(api_key_security)])
async def secure_endpoint():
    return {"message": "This is a secure endpoint"}


# --- API routes for Basic CRUD ---
# Get Paginated List of Packages using HTTP verb GET
@app.get('/packages/', dependencies=[Depends(api_key_security)], response_model=List[Package],
         status_code=status.HTTP_200_OK)
async def read_packages(skip: int = 0, take: int = 25):
    return await CRUDPackage(db_model, database).fetch_all(skip, take)


# Get single Package with its identifier using HTTP verb GET
@app.get('/packages/{package_id}/', dependencies=[Depends(api_key_security)], response_model=Package,
         status_code=status.HTTP_200_OK, summary='Read a Package')
async def read_packages(package_id: int):
    return await CRUDPackage(db_model, database).fetch_one(package_id)


# Create a new Package using HTTP verb POST
@app.post('/packages/', dependencies=[Depends(api_key_security)], response_model=Package,
          status_code=status.HTTP_201_CREATED, summary='Create a Package')
async def create_package(payload: PackageCreate):
    return await CRUDPackage(db_model, database).create(payload)


# Update Package using HTTP verb PUT
@app.put('/packages/{package_id}/', dependencies=[Depends(api_key_security)], response_model=Package,
         status_code=status.HTTP_200_OK, summary='Update a Package')
async def update_package(package_id: int, payload: PackageUpdate):
    return await CRUDPackage(db_model, database).update(package_id, payload)


# Delete single Package given its identifier using HTTP verb DELETE
@app.delete('/packages/{package_id}/', dependencies=[Depends(api_key_security)],
            status_code=status.HTTP_200_OK, summary='Delete a Package')
async def delete_package(package_id: int):
    return await CRUDPackage(db_model, database).delete(package_id)


# --- API routes for downloading or activating packages ---
# Update Package status after being downloaded using HTTP verb PUT
@app.put('/packages/downloaded/{package_id}/', dependencies=[Depends(api_key_security)], response_model=Package,
         status_code=status.HTTP_200_OK, summary='Report downloaded Package')
async def downloaded_package(package_id: int):
    return await CRUDPackage(db_model, database).evolve_status(package_id, DOWNLOADED)


# Update Package status after being activated using HTTP verb PUT
@app.put('/packages/activated/{package_id}/', dependencies=[Depends(api_key_security)], response_model=Package,
         status_code=status.HTTP_200_OK, summary='Report activated Package')
async def activated_package(package_id: int):
    return await CRUDPackage(db_model, database).evolve_status(package_id, ACTIVATED)
