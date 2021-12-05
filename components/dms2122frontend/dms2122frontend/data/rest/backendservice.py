""" BackendService class module.
"""

from typing import Optional
import requests
from dms2122common.data import Role
from dms2122common.data.rest import ResponseData
from typing import Optional

from dms2122frontend.data.rest.authservice import AuthService


class BackendService():
    """ REST client to connect to the backend service.
    """

    def __init__(self,
        host: str, port: int,
        api_base_path: str = '/api/v1',
        apikey_header: str = 'X-ApiKey-Backend',
        apikey_secret: str = ''
        ):
        """ Constructor method.

        Initializes the client.

        Args:
            - host (str): The backend service host string.
            - port (int): The backend service port number.
            - api_base_path (str): The base path that is prepended to every request's path.
            - apikey_header (str): Name of the header with the API key that identifies this client.
            - apikey_secret (str): The API key that identifies this client.
        """
        self.__host: str = host
        self.__port: int = port
        self.__api_base_path: str = api_base_path
        self.__apikey_header: str = apikey_header
        self.__apikey_secret: str = apikey_secret

    def __base_url(self) -> str:
        return f'http://{self.__host}:{self.__port}{self.__api_base_path}'

    def create_question(self, question:str,description:str,option1:str,option2:str,true_answer:str,correct_question_percentage:float,incorrect_question_percentage:float) -> ResponseData:
        """ Requests a user creation.

        Args:
            - token (Optional[str]): The user session token.
            - username (str): The new user's name.
            - password (str): The new user's password.

        Returns:
            - ResponseData: If successful, the contents hold the new user's data.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + '/question/add',
            json={
                'question': question,
                'description': description,
                'opt1': option1,
                'opt2': option2,
                'correct_answer': true_answer,
                'correct_answer_percentage': correct_question_percentage,
                'incorrect_answer_percentage': incorrect_question_percentage
            },
            headers={
                'Authorization': f'Bearer User',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data
