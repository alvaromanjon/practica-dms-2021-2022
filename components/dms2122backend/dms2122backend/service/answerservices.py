""" AnswerServices class module.
"""

from typing import Union, List
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.data.db import Schema
from dms2122backend.data.db.results import Answer
from dms2122backend.data.db.resultsets import Answers


class AnswerServices():
    """ Monostate class that provides high-level services to handle role-related use cases.
    """

    @staticmethod
    def create(user: str, answer: str, questionId: int, schema: Schema) -> None:
        """Answer a question.

        Args:
            - user (str): The user name string.
            - answer (str): The answer to the question.
            - questionid (int): Question answered.
            - schema (Schema): A database handler where answers are mapped into.

        """
        session: Session = schema.new_session()
        try:
            Answers.create(session, user, answer, questionId)

        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()

    @staticmethod
    def list_all(schema: Schema) -> List[Answer]:
        """Lists all the questions.

        Args:
            - schema (Schema): A database handler where users and roles are mapped into.

        Returns:
            - List[str]: The list of answers.
        """
        session: Session = schema.new_session()
        answers = Answers.list_all(session)
        schema.remove_session()
        return answers

    @staticmethod
    def list_all_by_question(schema: Schema, questionId: int) -> List[Answer]:
        """Lists the `Answer`s assigned to a question.

        Args:
            - schema (Schema): A database handler where users and roles are mapped into.
            - questionId (int): The question identifier.

        Returns:
            - List[Answer]: The list of answers.
        """
        session: Session = schema.new_session()
        answers = Answers.list_all_by_question(session, questionId)
        schema.remove_session()
        return answers

    @staticmethod
    def list_all_by_user(schema: Schema, user: str) -> List[Answer]:
        """Lists the `Answer`s assigned to a certain user.

        Args:
            - schema (Schema): A database handler where users and roles are mapped into.
            - user (str): The user name string.

        Returns:
            - List[Answer]: The list of answers.
        """
        session: Session = schema.new_session()
        answers = Answers.list_all_by_user(session, user)
        schema.remove_session()
        return answers