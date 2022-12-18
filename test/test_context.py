# -*- coding: utf-8 -*-

# --- Python modules ---
# sys: module which provides access to some variables used or maintained by the interpreter and to functions that
#      interact strongly with the interpreter.
from sys import argv

# constants
DEFAULT_BASE_URL = 'http://127.0.0.1:8000/'  # API Base URL
DEFAULT_API_KEY = 'fbd1d865-9ae8-491f-98b8-1f522c52eb02'  # API key for authentication


class TestContext:
    """
    This class collect several data to support testing tasks
    """

    def __init__(self,
                 base_url: str = DEFAULT_BASE_URL,
                 api_key: str = DEFAULT_API_KEY):
        """
        Class constructor
        :param base_url: API Base URL
        :param api_key: API key for authentication
        """
        self.base_url = base_url
        self.api_key = api_key
        self.log_file = './test.log'

        # Init API endpoints
        self.secure_endpoint = f'{self.base_url}secure'
        self.basic_crud_endpoint = f'{self.base_url}packages/'
        self.downloaded_endpoint = f'{self.basic_crud_endpoint}downloaded/'
        self.activated_endpoint = f'{self.basic_crud_endpoint}activated/'

        # Init headers for http requests
        self.request_headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'api-key': self.api_key,
        }

        # Properties for downloading and activating stub
        self.create_json_response = ''
        self.downloaded_json_response = ''
        self.activated_json_response = ''

    def customize(self):
        """
        Process command line parameters to take Base URL and API Key customized
        """
        # sys.argv is the array of command line parameters, where sys.argv[0] is the name of the PY program
        param_count_ = len(argv)
        if param_count_ > 1:
            for i in range(1, param_count_):
                try:
                    param_ = argv[i].upper()

                    if param_[0:2] == "-U":
                        # Get API base URL
                        next_param_ = argv[i + 1].lower()
                        if next_param_[0:4] == 'http':
                            self.base_url = next_param_

                    elif param_[0:2] == "-K":
                        # Get API key for authentication
                        next_param_ = argv[i + 1].lower()
                        if next_param_[0:1] != '-':
                            self.api_key = next_param_
                except Exception as e:
                    print(str(e))

        self.secure_endpoint = f'{self.base_url}secure'
        self.basic_crud_endpoint = f'{self.base_url}packages/'
        self.downloaded_endpoint = f'{self.basic_crud_endpoint}downloaded/'
        self.activated_endpoint = f'{self.basic_crud_endpoint}activated/'
