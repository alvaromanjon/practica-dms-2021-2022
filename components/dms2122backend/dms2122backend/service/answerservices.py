""" AnswerServices class module.
"""

from typing import Dict, Union, List
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.data.db import Schema
from dms2122backend.data.db.results import Answer
from dms2122backend.data.db.resultsets import Answers


class AnswerServices():
    """ Monostate class that provides high-level services to handle answer-related use cases.
    """

    @staticmethod
    def create(user: str, answer: str, questionId: int, schema: Schema) -> Dict:
        """Answer a question.

        Args:
            - user (str): The user name string.
            - answer (str): The answer to the question.
            - questionid (int): Question answered.
            - schema (Schema): A database handler where answers are mapped into.

        Raises:
            - ex: If the answer can't be created.

        Returns:
            - Dict: A dictionary with the new answer's data.
        """
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            newAnswer = Answers.create(session, user, answer, questionId)
            if newAnswer is not None:
                out['user'] = newAnswer.user
                out['questionId'] = newAnswer.questionId
                out['answer'] = newAnswer.answer

        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()

    @staticmethod
    def list_all_by_question(schema: Schema, questionId: int) -> List[Dict]:
        """Lists the `Answer`s assigned to a question.

        Args:
            - schema (Schema): A database handler where questions and answers are mapped into.
            - questionId (int): The question identifier.

        Returns:
            - List[Answer]: The list of answers.
        """
        session: Session = schema.new_session()
        out: List[Dict] = []
        answersReturned: List[Answer] = Answers.list_all_by_question(session, questionId)
        for eachAnswer in answersReturned:
            out.append({
                'user': eachAnswer.user,
                'questionId': eachAnswer.questionId,
                'answer': eachAnswer.answer
            })
        schema.remove_session()
        return out

    @staticmethod
    def list_all_by_user(schema: Schema, user: str) -> List[Answer]:
        """Lists the `Answer`s assigned to a certain user.

        Args:
            - schema (Schema): A database handler where questions and answers are mapped into.
            - user (str): The user.

        Returns:
            - List[Answer]: The list of answers.
        """
        session: Session = schema.new_session()
        out: List[Dict] = []
        answersReturned: List[Answer] = Answers.list_all_by_user(session, user)
        for eachAnswer in answersReturned:
            out.append({
                'user': eachAnswer.user,
                'questionId': eachAnswer.questionId,
                'answer': eachAnswer.answer
            })
        schema.remove_session()
        return out

    @staticmethod
    def get_answer(schema: Schema, user: str, questionId: int) -> Dict:
        """Returns an answer (if exists).

        Args:
            - schema (Schema): A database handler where the questions are mapped into.
            - user (str): The user that has answered the question.
            - questionId (int): Question identifier.

        Raises:
            - ex: If the answer hasn't been made.

        Returns:
            - out: Dictionary with all the answer's data.
            - None: If the answer doesn't exists.
        """
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            questionAnswered = Answers.get_answer(session, user, questionId)
            if questionAnswered is not None:
                out['user'] = questionAnswered.user
                out['questionId'] = questionAnswered.questionId
                out['answer'] = questionAnswered.answer
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out