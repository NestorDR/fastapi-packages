# -*- coding: utf-8 -*-

# --- Third Party Libraries ---
# requests: package that allows to make HTTP requests
from requests import get, post, put, delete, models

# --- Python modules ---
# datetime: module which provides classes for simple and complex date and time manipulation.
from datetime import datetime
# inspect: module which provides several useful functions to help get information about live objects such as modules,
#          classes, methods, functions, tracebacks, frame objects, and code objects
import inspect
# json: module which encode Python objects as JSON strings, and decode JSON strings into Python objects
from json import dumps
# logging: module which allows log debug lines, information, warnings, errors and critical errors to a log file
import logging
# os: module which allows access to functionalities dependent on the Operating System.
from os import path, remove
# random: module which implements pseudo-random number generators
import random
# sys: module which provides access to some variables used or maintained by the interpreter and to functions that
#      interact strongly with the interpreter.
from sys import exit

# --- Test modules ---
from test_context import TestContext


def report_response(test_description: str,
                    function_name: str,
                    response_body: models.Response):
    json = dumps(response_body.json(), indent=4)
    # json = response_body.json()
    result = f'{test_description} - (function {function_name}) \n{json}\n'
    print(result)

    # Logging to a file
    logger.info(result)


def test_apikey():
    test_name = inspect.stack()[0][0].f_code.co_name
    test_description = f'## Try HTTP GET using a valid API key {test_context.api_key}'
    response_body = \
        get(url=f'{test_context.secure_endpoint}', headers=test_context.request_headers)
    report_response(test_description, test_name, response_body)

    invalid_api_key = 'foo-foo-foo-foo'
    test_description = f'## Try HTTP GET using a invalid API key {invalid_api_key}'
    response_body = \
        get(url=f'{test_context.secure_endpoint}',
            headers={**test_context.request_headers, 'api-key': invalid_api_key})
    report_response(test_description, test_name, response_body)


def test_get_all():
    global package_id
    test_name = inspect.stack()[0][0].f_code.co_name
    params = {'skip': 0, 'take': 3}
    test_description = f'## Get paginated list of Packages using HTTP GET ' \
                       f'(offset/skip: {params["skip"]}, limit/take: {params["take"]})'
    response_body = \
        get(url=f'{test_context.basic_crud_endpoint}', headers=test_context.request_headers, params=params)
    report_response(test_description, test_name, response_body)

    # Extract identifier of the last package, for the next test
    package = response_body.json()[-1]
    package_id = package['id']


def test_get_one():
    global package_id
    test_name = inspect.stack()[0][0].f_code.co_name
    test_description = f'## Get a single Package with identifier {package_id} using HTTP verb GET'
    response_body = \
        get(url=f'{test_context.basic_crud_endpoint}{package_id}', headers=test_context.request_headers)
    report_response(test_description, test_name, response_body)

    bad_id = -1
    test_description = f'## Request a nonexistent package with identifier {bad_id} using HTTP verb GET'
    response_body = \
        get(url=f'{test_context.basic_crud_endpoint}{bad_id}', headers=test_context.request_headers)
    report_response(test_description, test_name, response_body)


def test_create():
    global package_id
    test_name = inspect.stack()[0][0].f_code.co_name
    test_description = f'## Create a package using HTTP verb POST'
    random.seed(datetime.now().timestamp())  # Set random seed to generate a random version number
    payload = {
        'name': datetime.now().strftime('Package created in test on %Y-%m-%d %H:%M'),
        'version': f'0.{random.randint(1, 9)}.{random.randint(1, 20)}'
    }
    response_body = \
        post(url=f'{test_context.basic_crud_endpoint}', headers=test_context.request_headers, json=payload)
    report_response(test_description, test_name, response_body)
    package = response_body.json()
    package_id = package['id']

    test_description = f'## Create a packet with an empty value in the attribute name, using the HTTP POST verb'
    response_body = \
        post(url=f'{test_context.basic_crud_endpoint}', headers=test_context.request_headers,
             json={**payload, 'name': ""})              # Empty name
    report_response(test_description, test_name, response_body)


def test_update():
    global package_id
    test_name = inspect.stack()[0][0].f_code.co_name
    test_description = f'## Update package with identifier {package_id} using HTTP verb PUT'
    payload = {
        'name': datetime.now().strftime('Package updated in test on %Y-%m-%d %H:%M'),
        'version': f'0.{random.randint(1, 9)}.{random.randint(1, 20)}',
        'status_id': 1                                  # 1.Created
    }
    response_body = \
        put(url=f'{test_context.basic_crud_endpoint}{package_id}', headers=test_context.request_headers, json=payload)
    report_response(test_description, test_name, response_body)

    test_description = f'## Update package with identifier {package_id} and bad status_id, using HTTP verb PUT'
    response_body = \
        put(url=f'{test_context.basic_crud_endpoint}{package_id}', headers=test_context.request_headers,
            json={**payload, 'status_id': 9})           # Status with identifier 9 doesn't exist
    report_response(test_description, test_name, response_body)

    bad_id = -1
    test_description = f'## Update a nonexistent package with identifier {bad_id} using HTTP verb PUT'
    response_body = \
        put(url=f'{test_context.basic_crud_endpoint}{bad_id}', headers=test_context.request_headers, json=payload)
    report_response(test_description, test_name, response_body)


def test_delete():
    global package_id
    test_name = inspect.stack()[0][0].f_code.co_name
    test_description = f'## Delete a single Package with identifier {package_id} using HTTP verb DELETE'
    response_body = \
        delete(url=f'{test_context.basic_crud_endpoint}{package_id}', headers=test_context.request_headers)
    report_response(test_description, test_name, response_body)


# Use of __name__ & __main__
# When the Python interpreter reads a code file, it completely executes the code in it.
# For example, in a file my_module.py, when executed as the main program, the __name__ attribute will be '__main__',
# however if it is used importing it from another module: import my_module, the __name__ attribute will be 'my_module'.
if __name__ == '__main__':
    # Create test context to store context and results
    test_context = TestContext()

    # Process command line parameters to take Base URL and API Key customized
    test_context.customize()

    # Show API execution context
    print('API context')
    print(f'API Base URL .............: {test_context.base_url}')
    print(f'API key for authentication: {test_context.api_key}')

    # Delete previous log file
    if path.exists(test_context.log_file):
        remove(test_context.log_file)

    # Setup logging to a file
    logger = logging.getLogger('testlogger')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(filename=test_context.log_file)
    logger.addHandler(file_handler)

    #
    test_apikey()

    package_id = None
    test_get_all()

    if package_id is not None:
        test_get_one()

    test_create()

    test_update()

    test_delete()

    logger.removeHandler(file_handler)

    # Terminate normally
    exit(0)
