# -*- coding: utf-8 -*-
"""
Since downloading or activating a package could be long operations, these operations are simulated with this Stub script
"""
# --- Third Party Libraries ---
# tdgm: library which shows smart progress meter
from tqdm import tqdm

# --- Python modules ---
# datetime: module which provides classes for simple and complex date and time manipulation.
from datetime import datetime
# json: module which encode Python objects as JSON strings, and decode JSON strings into Python objects
from json import dumps
# random: module which implements pseudo-random number generators
import random
# requests: module that allows to make HTTP requests
from requests import post, put
# sys: module which provides access to some variables used or maintained by the interpreter and to functions that
#      interact strongly with the interpreter.
from sys import exit
# time: module which provides various time-related functions.
from time import sleep

# --- Test modules ---
from test_context import TestContext


def create_package():
    # Create new package, later it will be downloaded and activated
    print('\nCreating package...')
    random.seed(datetime.now().timestamp())  # Set random seed to generate a random version number
    payload = {
        'name': datetime.now().strftime('Package stubbed on %Y-%m-%d %H:%M'),
        'version': f'0.{random.randint(1, 9)}.{random.randint(1, 20)}'
    }
    # API call to create new package
    test_context.create_json_response = \
        post(url=f'{test_context.basic_crud_endpoint}', headers=test_context.request_headers, json=payload).json()


def download_package():
    # Stub download package
    print('\nDownloading package...')
    for _ in tqdm(range(20), ncols=70):
        sleep(0.2)
    # API call to report downloaded package
    test_context.downloaded_json_response = \
        put(url=f'{test_context.downloaded_endpoint}{package_id}', headers=test_context.request_headers).json()


def activate_package():
    # Stub activate package
    print('\nActivating package...')
    for _ in tqdm(range(20), ncols=70):
        sleep(0.1)
    # API call to report activated package
    test_context.activated_json_response = \
        put(url=f'{test_context.activated_endpoint}{package_id}', headers=test_context.request_headers).json()


def show_results():
    # Show the results of the API calls, like beautified JSON
    print('\nSTUB Resume')
    print(f'Package creation results: {dumps(test_context.create_json_response, indent=4)}')
    print(f'Package download results: {dumps(test_context.downloaded_json_response, indent=4)}')
    print(f'Package activate results: {dumps(test_context.activated_json_response, indent=4)}')


# Use of __name__ & __main__
# When the Python interpreter reads a code file, it completely executes the code in it.
# For example, in a file my_module.py, when executed as the main program, the __name__ attribute will be '__main__',
# however if it is used importing it from another module: import my_module, the __name__ attribute will be 'my_module'.
if __name__ == '__main__':
    # Create test context object to store API execution context and results
    test_context = TestContext()

    # Process command line parameters to take Base URL and API Key customized
    test_context.customize()

    # Show API execution context
    print('API context')
    print(f'API Base URL .............: {test_context.base_url}')
    print(f'API key for authentication: {test_context.api_key}')

    # Create new package, later it will be downloaded and activated
    create_package()

    # Extract the identifier of the new package, for the next API calls
    package_id = test_context.create_json_response['id']

    # Invoke stub download package
    download_package()

    # Invoke stub activate package
    activate_package()

    # Show the results of the API calls, like beautified JSON
    show_results()

    # Terminate normally
    exit(0)
