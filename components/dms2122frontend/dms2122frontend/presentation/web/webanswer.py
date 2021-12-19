from typing import Dict, List, Optional
from flask import session
from dms2122common.data.rest import ResponseData
from dms2122frontend.data.rest.backendservice import BackendService
from .webutils import WebUtils

class WebAnswer():
    """ Monostate class responsible of the question operation utilities.
    """


    @staticmethod
    def answer_question(backend_service: BackendService, user: str, questionId: int, answer: str) -> Optional[Dict]:
        """ Answers a question in the backend service.

        Args:
            - backend_service (BackendService): The backend service.
            - user (str): A string with the user.
            - answer (str): A string with the question's answer putted by student.
            - questionId (str): A string with the questionId of the question.

        Returns:
            - Dict: A dictionary with the newly created question if successful.
            - None: Nothing on error.
        """
        response: ResponseData = backend_service.answer_question(session.get('token'), user, questionId, answer)
        WebUtils.flash_response_messages(response)
        return response.get_content()

    @staticmethod
    def list_answers_to_question(backend_service: BackendService, questionId: int) -> List:
        """ Gets the list of questions from the backend service.

        Args:
            - backend_service (BackendService): The backend service.

        Returns:
            - List: A list of question data dictionaries (the list may be empty)
        """
        response: ResponseData = backend_service.list_answers_to_question(session.get('token'),questionId)
        WebUtils.flash_response_messages(response)
        if response.get_content() is not None and isinstance(response.get_content(), list):
            return list(response.get_content())
        return []

    @staticmethod
    def list_answers_from_user(backend_service: BackendService, user:str) -> List:
        """ Gets the list of questions from the backend service.

        Args:
            - backend_service (BackendService): The backend service.

        Returns:
            - List: A list of question data dictionaries (the list may be empty)
        """
        response: ResponseData = backend_service.list_answers_to_question(session.get('token'),user)
        WebUtils.flash_response_messages(response)
        if response.get_content() is not None and isinstance(response.get_content(), list):
            return list(response.get_content())
        return []


