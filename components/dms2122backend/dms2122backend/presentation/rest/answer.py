""" REST API controllers responsible of handling the answer operations.
"""

from typing import Tuple, Union, Optional, List, Dict
from http import HTTPStatus
from flask import current_app # type: ignore
from dms2122backend.data.db.exc import QuestionNotFoundError
from dms2122backend.service import AnswerServices
from dms2122backend.data.db.results import Answer
from dms2122common.data.role import Role


def create_answer(body: Dict, token_info: Dict) -> Tuple[Union[Dict, str], Optional[int]]:
    """Answers a question.

    Args:
        - body (Dict): A dictionary with the new answer's data.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[Dict, str], Optional[int]]: A tuple with no content and codes:
            - 200 OK if the question is answered.
            - 400 BAD REQUEST when a mandatory argument is missing.
            - 404 NOT FOUND if the question doesn't exist.
    """
    with current_app.app_context():
        try:
            newAnswer: Dict = AnswerServices.create(body['user'], body['answer'], 
                                        body['questionId'], current_app.db)
            
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
        except QuestionNotFoundError:
            return ('The question does not exist', HTTPStatus.NOT_FOUND.value)
    return (newAnswer, HTTPStatus.OK.value)

def list_answers_by_question(questionId: int) -> Tuple[Union[List[Dict], str], Optional[int]]:
    """Lists the existing answers by question.

    Returns:
        - Tuple[Union[List[Dict], str], Optional[int]]: A tuple with a list of dictionaries for the answers' data
          and code:
        - 200 OK if the answers have been returned.
        - 400 BAD REQUEST when a mandatory argument is missing.
        - 404 NOT FOUND if the question doesn't exist.
    """
    with current_app.app_context():
        try:
            answersListed: List[Dict] = AnswerServices.list_all_by_question(current_app.db, questionId)
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
        except QuestionNotFoundError:
            return ('The question does not exist', HTTPStatus.NOT_FOUND.value)
    return (answersListed, HTTPStatus.OK.value)

def list_answers_by_user(user: str) -> Tuple[Union[List[Dict], str], Optional[int]]:
    """Lists the existing answers by user.

    Returns:
        - Tuple[Union[List[Dict], str], Optional[int]]: A tuple with a list of dictionaries for the answers' data
          and code:
        - 200 OK if the answers have been returned.
        - 400 BAD REQUEST when a mandatory argument is missing.
        - 404 NOT FOUND if the user doesn't exist.
    """
    with current_app.app_context():
        try:
            answersListed: List[Dict] = AnswerServices.list_all_by_user(current_app.db, user)
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
        except QuestionNotFoundError:
            return ('The user does not exist', HTTPStatus.NOT_FOUND.value)
    return (answersListed, HTTPStatus.OK.value)

def get_answer(user: str, questionId: int) -> Tuple[Union[Dict, str], Optional[int]]:
    """Gets the answer of a question.

    Returns:
        - Tuple[Union[Dict, str], Optional[int]]: A tuple with a list of dictionaries for the answers' data
          and code:
        - 200 OK if the answers have been returned.
        - 400 BAD REQUEST when a mandatory argument is missing.
        - 404 NOT FOUND if the user doesn't exist.
    """
    with current_app.app_context():
        try:
            answerReturned: Dict = AnswerServices.get_answer(current_app.db, user, questionId)
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
        except QuestionNotFoundError:
            return ('The question does not exist', HTTPStatus.NOT_FOUND.value)
    return (answerReturned, HTTPStatus.OK.value)