""" REST API controllers responsible of handling the answer operations.
"""

from typing import Tuple, Union, Optional, List, Dict
from http import HTTPStatus
from flask import current_app # type: ignore
#from dms2122auth.service.roleservices import RoleServices # type: ignore
from dms2122backend.data.db.exc import QuestionNotFoundError
from dms2122backend.service import AnswerServices
from dms2122backend.data.db.results import Answer
from dms2122common.data.role import Role


def create_answer(body: Dict, token_info: Dict) -> Tuple[Optional[str], Optional[int]]:
    """Answers a question.

    Args:
        - body (Dict): A dictionary with the new answer's data.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Optional[str], Optional[int]]: A tuple with no content and codes:
            - 200 if the question is answered.
            - 404 if the question doesn't exist.
    """
    with current_app.app_context():
        if not RoleServices.has_role(token_info['user_token']['user'], Role.Student, current_app.db):
            return (
                'Current user has not enough privileges to answer a question',
                HTTPStatus.FORBIDDEN.value
            )
        try:
            AnswerServices.create(body['user'], body['answer'], 
                                        body['questionId'], current_app.db)
            
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
        except QuestionNotFoundError:
            return ('The question does not exist', HTTPStatus.NOT_FOUND.value)
    return (None, HTTPStatus.OK.value)

def list_answers() -> Tuple[Union[List[Answer], str], Optional[int]]:
    """Lists the existing answers.

    Returns:
        - Tuple[Union[List[Answer], str], Optional[int]]: A tuple with a list of dictionaries for the questions' data
          and a code 200 OK.
    """
    with current_app.app_context():
        answers: List[Answer] = AnswerServices.list_all(current_app.db)
    return (answers, HTTPStatus.OK.value)

def list_answers_by_question(questionId: int) -> Tuple[Union[List[Answer], str], Optional[int]]:
    """Lists the existing answers by question.

    Returns:
        - Tuple[Union[List[Answer], str], Optional[int]]: A tuple with a list of dictionaries for the questions' data
          and a code 200 OK.
    """
    with current_app.app_context():
        answers: List[Answer] = AnswerServices.list_all_by_question(current_app.db, questionId)
    return (answers, HTTPStatus.OK.value)

def list_answers_by_user(user: str) -> Tuple[Union[List[Answer], str], Optional[int]]:
    """Lists the existing answers by user.

    Returns:
        - Tuple[Union[List[Answer], str], Optional[int]]: A tuple with a list of dictionaries for the questions' data
          and a code 200 OK.
    """
    with current_app.app_context():
        answers: List[Answer] = AnswerServices.list_all_by_user(current_app.db, user)
    return (answers, HTTPStatus.OK.value)

