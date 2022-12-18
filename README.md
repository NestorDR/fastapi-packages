# Project Description fastapi-packages 

This project was created to meet the following technical challenge:

    Create a REST API in C# or Python for managing software packages with the following requirements:

    - A software package has a name, version and status
    - You need to be able to create, remove, edit and list packages.
    - A package has one of the following statuses:
           Created: created and defined but not yet locally available
           Downloaded: locally available but not yet activated
           Active: in use
    - Think of a way to change the status of a package, but take into account that downloading
        or activating a package is a long operation (the implemented method itself can be a stub)
    - Secure the API with API key authentication and build API key management (creating, 
        deleting and deactivating keys)
    - Choose your backend storage technology of choice. Motivate your choice.
    - Add some tests and a way to package and deploy your software as a Docker container.

# REST API in Python for managing software packages

## The API

I chose Python for the implementation, relying on the large and proven ecosystem of modern libraries available. And as for C#, its libraries are usually very well documented, although its ecosystem perhaps seems a bit less broad.

As for web frameworks for the API, I evaluated [Flask](https://flask.palletsprojects.com/en/2.1.x/) vs [FastAPI](https://fastapi.tiangolo.com/) as alternatives, and preferred the latter as it is clearly designed for building APIs. Also, soon I discovered that it is easier to implement securitization with API keys in FastAPI.

I chose to work with relational databases, and decided to implement an asynchronous CRUD. It is usually easier to develop a synchronous API however, when working with large volumes of data, the asynchronous operations are more efficient. The logo of the company offering the technical challenge says: **create value from data**. Many data? Let me try an asynchronous solution. 

Thus, I selected the library [Databases](https://www.encode.io/databases/), which gives us simple asynchronous I/O (asyncio) support for databases. It allows us to make queries using [SQLAlchemy Core](https://docs.sqlalchemy.org/en/14/core/index.html) expression language, and provides support for PostgreSQL, MySQL, and SQLite.

I tried to implement the project following the best practices. The code is highly commented for easy understanding. 

### Development platform
Python 3.10.4 on Windows 11 

### Requirements
```
pip install -r requirements.txt  
```

### Run it 
I developed CMD file `.\runAPI.cmd` to run on Windows Command Prompt (cmd), just run:
```
runAPI.cmd
```
Inside CMD file, the command to run the FastAPI is
```
uvicorn --port 8000 --host 127.0.0.1 app.main:app --reload
```

### Interactive API docs
Now go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

You will see the automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui)):

![FastAPI Documentation](/img/fastapi_packages_docs.png "FastAPI Documentation")

Or alternatively you can see the automatic documentation (provided by [ReDoc](https://github.com/Redocly/redoc)) on [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

## CRUD

The implementation allows to create, delete, edit and list packages, as well as include methods to evolve the status of packages after download and activation.

## Entity Package
The app's data schema is implemented with the [pydantic](https://pydantic-docs.helpmanual.io/) library (used by FastAPI) which provides data validation and configuration management using Python like hints/annotations. Therefore, `Package`, the main entity of the application is defined as follows:  
```python
# app/schemas/package.py
from pydantic import BaseModel

class Package(BaseModel):
    id: int
    name: str
    version: str
    status: str
``` 

## Statuses of each Package: Created, Downloaded or Active
Its implementation could have been done with enumerations (Python's Enum class), but I have opted for a new entity/table, `Statuses` that will allow new ones without the need to modify the source code, e.g. Rejected. Additionally, it could show a 1 to N relationship implementation as follows (defined like SQLAlchemy Core Table):
```python
# app/models/statuses.py

from sqlalchemy import Table, Column, ForeignKey, Integer, String

# table representation Statuses
self.table = Table(
	'statuses',
	self.metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(length=20), nullable=False),
)

...

# app/models/packages.py

# table representation Packages
self.table = Table(
	'packages',
	self.metadata,
	Column('id', Integer, primary_key=True),
	Column('name', String(length=200), nullable=False),
	Column('version', String(length=50), nullable=False),
	Column('status_id', Integer, ForeignKey("statuses.id"), nullable=False),
)
```

## API Securitization with API key authentication 
The project implements the use of the [FastAPI simple security](https://github.com/mrtolkien/fastapi_simple_security/) library that offers:
- Key creation, revocation, renewing, and usage logs handled through administrator endpoints
- API key security with local SQLite backend, working with both header and query parameters
- Configurable deprecation days for generated API keys 

![FastAPI simple security](/img/fastapi_simple_security.png "FastAPI simple security")

FastAPI simple security, use a secret administrator key that allows API key management. it can be set via the environment variable `FASTAPI_SIMPLE_SECURITY_SECRET`, in development it can be seen in the command file `runAPI.cmd`. But if not provided, it is generated automatically on server startup.  

Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) and inform an API Key in the Authorize/Query or Header box. For app testing use API Key: `fbd1d865-9ae8-491f-98b8-1f522c52eb02` already configured in SQLite backend.

![Setting API Key](/img/set_apikey.png "Setting API Key")

## Downloading or activating a package

Downloading packages, can be running a Windows Update or running a Python pip. I have implemented the Stub script `./test/stub_DA.py`, that simulates the download and activation by console. Obviously the Rest API must be working for the stub to work.

### Run it
On Windows Command Prompt (cmd):
```
runStubDA.cmd
```
Inside CMD file, the base URL of the API and the API Key are passed as command line parameters.
```
py test/stub_DA.py -U http://127.0.0.1:%PORT%/ -K fbd1d865-9ae8-491f-98b8-1f522c52eb02
```

![Downloading and activating](/img/downloading_activating.png "Downloading and activating")

## Backend storage technology

The challenge data schema is small, and is perfectly suited to be stored in a relational database.

The supported database engines are SQLite and PostgresSQL, both free of charge.  Both have been tested during development.

The `FASTAPI_PACKAGES_DB_ENGINE` environment variable, allows you to set the desired engine, in development that can be seen in the command file `runAPI.cmd`

The implementation is deployed with SQLite.
```
# app/db_engines/sqlite.py

# Configure SQLite Database Connection String
DATABASE_URL = "sqlite:///packages.db"
```

But if you want to use PostgreSQL you must configure the environment variables that appear in the following snippet:
```
# app/db_engines/postgresql.py

# Configure PostgreSQL Database Connection String
host_server = environ.get('POSTGRESQL_SERVER', 'localhost')
db_server_port = parse.quote_plus(str(environ.get('POSTGRESQL_SERVER_PORT', '5432')))
database_name = environ.get('POSTGRESQL_DATABASE_NAME', 'packages')
db_username = parse.quote_plus(str(environ.get('POSTGRESQL_USERNAME', 'postgres')))
db_password = parse.quote_plus(str(environ.get('POSTGRESQL_PASSWORD', 'password')))
ssl_mode = parse.quote_plus(str(environ.get('POSTGRESQL_SSL_MODE', 'prefer')))
DATABASE_URL = \
    f'postgresql://{db_username}:{db_password}@{host_server}:{db_server_port}/{database_name}?sslmode={ssl_mode}'
```

## Some tests

I have developed the `.test/test_valid_api.py` script which implements some unit tests. The results are displayed on the screen and saved in the log file `./test.log`.

### Run it
On Windows Command Prompt (cmd):
```
runTest.cmd
```
Inside CMD file, the base URL of the API and the API Key are passed as command line parameters.
```
py test/test_valid_api.py -U http://127.0.0.1:%PORT%/ -K fbd1d865-9ae8-491f-98b8-1f522c52eb02
```

## Dockerizing

In the same project folder is created the file `Dockerfile`, containing all the commands needed to build a Docker image. The image will contain the two SQLite databases used by the project during the development stage. Remember the security API Key: `fbd1d865-9ae8-491f-98b8-1f522c52eb02`.

Also, I developed another 2 CMD files:
* `dockerBuild.cmd` to build an image called `ndr_fastapi_packages_image`

![Building Docker image](/img/ndr_fastapi_packages_image.png "Building Docker image")
* `dockerRun.cmd` to run a container called `ndr_fastapi_packages` based on image

### Check it
Now you can go to the [interactive API docs](http://127.0.0.1/docs) (or equivalent, using your Docker host).

### Stub and Test 
If you want to run the Stub or Test scripts developed, on the API deployed in the Docker container. Assuming you are using http://127.0.0.1/, simply run the CMD files with the `P` command line parameter, as shown below.

On Windows Command Prompt (cmd):
```
runStubDA.cmd P
```
or
```
runTest.cmd P
```
