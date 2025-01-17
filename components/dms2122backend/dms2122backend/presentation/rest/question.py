""" REST API controllers responsible of handling the question operations.
"""

from typing import Tuple, Union, Optional, List, Dict
from http import HTTPStatus
from dms2122backend.data.db.exc.questionnotfounderror import QuestionNotFoundError
from flask import current_app # type: ignore
from dms2122backend.data.db.exc import QuestionExistsError
from dms2122backend.service import QuestionServices 
from dms2122backend.data.db.results import Question
from dms2122common.data.role import Role

def create_question(body: Dict, token_info: Dict) -> Tuple[Union[Dict, str], Optional[int]]:
    """Creates a question if the user has the teacher role.

    Args:
        - body (Dict): A dictionary with the new question's data.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[Dict, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
            - 403 FORBIDDEN when the requestor does not have the rights to create the user.
            - 409 CONFLICT if an existing user already has all or part of the unique user's data.
    """
    with current_app.app_context():
        try:
            newQuestion: Dict = QuestionServices.create_question(body['question'],
            body['description'], body['option1'], body['option2'], body['true_answer'], 
            body['correct_question_percentage'], body['incorrect_question_percentage'], current_app.db)
            
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
        except QuestionExistsError:
            return ('The question already exists', HTTPStatus.CONFLICT.value)
    return (newQuestion, HTTPStatus.OK.value)

def list_questions() -> Tuple[List[Dict], Optional[int]]:
    """Lists the existing questions.

    Returns:
        - Tuple[List[Dict], Optional[int]]: A tuple with a list of dictionaries for the questions' data
          and a code 200 OK.
    """
    with current_app.app_context():
        questionsListed: List[Dict] = QuestionServices.list_questions(current_app.db)
    return (questionsListed, HTTPStatus.OK.value)

def get_question_id(questionId: int, token_info: Dict) -> Tuple[Union[Dict, str], Optional[int]]:
    """Get a question using the id.

    Args:
        - questionId (int): Question identifier.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[Dict, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
            - 404 NOT FOUND when the question doesn't exist.
    """
    with current_app.app_context():
        try:
            questionReturned: Dict = QuestionServices.get_question_id(questionId, current_app.db)
            
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
        except QuestionNotFoundError:
            return ('The question does not exist', HTTPStatus.NOT_FOUND.value)
    return (questionReturned, HTTPStatus.OK.value)

def edit_question(body: Dict, questionId: int, token_info: Dict) -> Tuple[Union[Dict, str], Optional[int]]:
    """Edits a question if the user has the teacher role.

    Args:
        - body (Dict): A dictionary with the new question's data.
        - questionId (int): Question identifier.
        - token_info (Dict): A dictionary of information provided by the security schema handlers.

    Returns:
        - Tuple[Union[Dict, str], Optional[int]]: On success, a tuple with the dictionary of the
          new question data and a code 200 OK. On error, a description message and code:
            - 400 BAD REQUEST when a mandatory argument is missing.
            - 403 FORBIDDEN when the requestor does not have the rights to create the user.
            - 404 NOT FOUND if the question doesn't exist.
    """
    with current_app.app_context():
        try:
            questionEdited: Dict = QuestionServices.edit_question(questionId, body['question'],
            body['description'], body['option1'], body['option2'], body['true_answer'], 
            body['correct_question_percentage'], body['incorrect_question_percentage'], current_app.db)
            
        except ValueError:
            return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)
        except QuestionNotFoundError:
            return ('The question does not exist', HTTPStatus.NOT_FOUND.value)
    return (questionEdited, HTTPStatus.OK.value)