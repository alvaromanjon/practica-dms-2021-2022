""" WebQuestion class module.
"""

from typing import Dict, List, Optional
from flask import session
from dms2122common.data.rest import ResponseData
from dms2122frontend.data.rest.backendservice import BackendService
from .webutils import WebUtils

class WebQuestion():
    """ Monostate class responsible of the question operation utilities.
    """

    @staticmethod
    def list_questions(backend_service: BackendService) -> List:
        """ Gets the list of questions from the backend service.

        Args:
            - backend_service (BackendService): The backend service.

        Returns:
            - List: A list of question data dictionaries (the list may be empty)
        """
        response: ResponseData = backend_service.list_questions(session.get('token'))
        WebUtils.flash_response_messages(response)
        if response.get_content() is not None and isinstance(response.get_content(), list):
            return list(response.get_content())
        return []

    @staticmethod
    def create_question(backend_service: BackendService, question:str, description:str, option1:str,
                        option2:str,true_answer:str,correct_question_percentage:str,
                        incorrect_question_percentage:str) -> Optional[Dict]:
        """ Creates a question in the backend service.

        Args:
            - backend_service (BackendService): The backend service.
            - question (str): A string with the question.
            - description (str): A string with the question's description.
            - option1 (str): A string with the first possible answer of the question.
            - option2 (str): A string with the second possible answer of the question.
            - true_answer (str): A string with the true answer of the question.
            - correct_question_percentage (float): A float with the percentage to be added in case of having the correct answer.
            - incorrect_question_percentage (float): A float with the percentage to be substracted in case of having the incorrect answer.

        Returns:
            - Dict: A dictionary with the newly created question if successful.
            - None: Nothing on error.
        """
        response: ResponseData = backend_service.create_question(session.get('token'), question, 
                                    description, option1, option2, true_answer, correct_question_percentage, 
                                    incorrect_question_percentage)
        WebUtils.flash_response_messages(response)
        return response.get_content()

    @staticmethod
    def edit_question(backend_service: BackendService, questionId: int, question:str, description:str, option1:str,
                        option2:str,true_answer:str,correct_question_percentage:str,
                        incorrect_question_percentage:str) -> Optional[Dict]:
        """ Creates a question in the backend service.

        Args:
            - backend_service (BackendService): The backend service.
            - questionId (int): Question identifier.
            - question (str): A string with the question.
            - description (str): A string with the question's description.
            - option1 (str): A string with the first possible answer of the question.
            - option2 (str): A string with the second possible answer of the question.
            - true_answer (str): A string with the true answer of the question.
            - correct_question_percentage (float): A float with the percentage to be added in case of having the correct answer.
            - incorrect_question_percentage (float): A float with the percentage to be substracted in case of having the incorrect answer.

        Returns:
            - Dict: A dictionary with the newly created question if successful.
            - None: Nothing on error.
        """
        response: ResponseData = backend_service.edit_question(session.get('token'), questionId, question, 
                                    description, option1, option2, true_answer, correct_question_percentage, 
                                    incorrect_question_percentage)
        WebUtils.flash_response_messages(response)
        return response.get_content()

    @staticmethod
    def get_question(backend_service: BackendService, questionId: int) -> List:
        """ Gets the list of questions from the backend service.

        Args:
            - backend_service (BackendService): The backend service.
            - questionId (int): Question identifier.

        Returns:
            - List: A list of question data dictionaries (the list may be empty)
        """
        response: ResponseData = backend_service.get_question(session.get('token'), questionId)
        WebUtils.flash_response_messages(response)
        return response.get_content()