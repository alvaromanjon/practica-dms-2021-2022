""" BackendService class module.
"""

from typing import Optional
import requests
from dms2122common.data import Role
from dms2122common.data.rest import ResponseData
from typing import Optional

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

    def list_questions(self, token: Optional[str]) -> ResponseData:
        """ Requests a list of registered questions.

        Args:
            token (Optional[str]): The user session token.

        Returns:
            - ResponseData: If successful, the contents hold a list of question data dictionaries.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + '/questions',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data


    def create_question(self, token: Optional[str], question:str, description:str, option1:str, 
                        option2:str, true_answer:str, correct_question_percentage:str, 
                        incorrect_question_percentage:str) -> ResponseData:
        """ Requests a question creation.

        Args:
            - token (Optional[str]): The user session token.
            - question (str): A string with the question.
            - description (str): A string with the question's description.
            - option1 (str): A string with the first possible answer of the question.
            - option2 (str): A string with the second possible answer of the question.
            - true_answer (str): A string with the true answer of the question.
            - correct_question_percentage (float): A float with the percentage to be added in case of having the correct answer.
            - incorrect_question_percentage (float): A float with the percentage to be substracted in case of having the incorrect answer.

        Returns:
            - ResponseData: If successful, the contents hold the new question's data.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + '/questions/add',
            json={
                'question': question,
                'description': description,
                'option1': option1,
                'option2': option2,
                'correct_answer': true_answer,
                'correct_answer_percentage': correct_question_percentage,
                'incorrect_answer_percentage': incorrect_question_percentage
            },
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def edit_question(self, token: Optional[str], questionId: int, question:str, description:str, option1:str, 
                        option2:str, true_answer:str, correct_question_percentage:str, 
                        incorrect_question_percentage:str) -> ResponseData:
        """ Requests to edit a question.

        Args:
            - token (Optional[str]): The user session token.
            - questionId (int): Question identifier.
            - question (str): A string with the question.
            - description (str): A string with the question's description.
            - option1 (str): A string with the first possible answer of the question.
            - option2 (str): A string with the second possible answer of the question.
            - true_answer (str): A string with the true answer of the question.
            - correct_question_percentage (float): A float with the percentage to be added in case of having the correct answer.
            - incorrect_question_percentage (float): A float with the percentage to be substracted in case of having the incorrect answer.

        Returns:
            - ResponseData: If successful, the contents hold the new question's data.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.put(
            self.__base_url() + f'/questions/{questionId}/edit',
            json={
                'questionId': questionId,
                'question': question,
                'description': description,
                'option1': option1,
                'option2': option2,
                'correct_answer': true_answer,
                'correct_answer_percentage': correct_question_percentage,
                'incorrect_answer_percentage': incorrect_question_percentage
            },
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def get_question(self, token: Optional[str], questionId: int) -> ResponseData:
        """ Requests a question.

        Args:
            - token (Optional[str]): The user session token.
            - questionId (int): Question identifier.

        Returns:
            - ResponseData: If successful, the contents hold a question.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/questions/{questionId}/preview',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def answer_question(self, token: Optional[str], user: str, questionId: int, answer: str) -> ResponseData:
        """ Answers a question.

        Args:
            - token (Optional[str]): The user session token.
            - user (str): The user that is answering the question.
            - questionId (int): Question identifier.
            - answer (str): The answer.

        Returns:
            - ResponseData: If successful, the contents hold a question.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f'/questions/{questionId}/answer/{user}',
            json={
                'user': user,
                'questionId': questionId,
                'answer': answer
            },
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def list_answers_to_question(self, token: Optional[str], questionId: int) -> ResponseData:
        """ List all the answers to a question.

        Args:
            - token (Optional[str]): The user session token.
            - questionId (int): Question identifier.

        Returns:
            - ResponseData: If successful, the contents hold a list of answers.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/questions/{questionId}/answers',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def list_answers_from_user(self, token: Optional[str], user: str) -> ResponseData:
        """ List all the answers made by an user.

        Args:
            - token (Optional[str]): The user session token.
            - user (str): An user.

        Returns:
            - ResponseData: If successful, the contents hold a list of answers.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/questions/{user}/answers',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def get_answer(self, token: Optional[str], user: str, questionId: int) -> ResponseData:
        """ Requests an answer.

        Args:
            - token (Optional[str]): The user session token.
            - user (str): An user.
            - questionId (int): Question identifier.

        Returns:
            - ResponseData: If successful, the contents hold an answer.
              Otherwise, the contents will be an empty list.
        """
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/questions/{user}/answers/{questionId}',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            }
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data


