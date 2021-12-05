""" Answers class module.
"""

from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2122backend.data.db.exc import QuestionNotFoundError  # type: ignore
from dms2122auth.data.db.results import Answer
from dms2122backend.data.db.results import question


class Answers():
    """ Class responsible of table-level answers operations.
    """
    @staticmethod
    def create(session: Session, user: str, answer: str, questionId: int) -> Answer:
        """ Grants a role to a user.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - user (str): The user name string.
            - answer (str): The answer to the question.
            - questionid (int): Question answered.

        Raises:
            - ValueError: If any field is missing.
            - QuestionNotFoundError: If the question doesn't exist.

        Returns:
            - Answer: The created `Answer` result.
        """
        if not user or not answer or not questionId:
            raise ValueError('A user, answer and questionId are required.')
        try:
            new_answer = Answer(user, answer, questionId)
            session.add(new_answer)
            session.commit()
            return new_answer
        except IntegrityError as ex:
            session.rollback()
            raise QuestionNotFoundError() from ex
        except:
            session.rollback()
            raise

    @staticmethod
    def list_all(session: Session) -> List[Answer]:
        """Lists every Answer.

        Args:
            - session (Session): The session object.

        Returns:
            - List[Answer]: A list of all `Answer`.
        """

        query = session.query(Answer)
        return query.all()

    @staticmethod
    def list_all_by_question(session: Session, questionId: int) -> List[Answer]:
        """Lists the `Answer`s assigned to a question.

        Args:
            - session (Session): The session object.
            - questionId (int): The question identifier.

        Raises:
            - ValueError: If the question is missing.

        Returns:
            - List[Answer]: A list of `Answer` registered with the question.
        """
        if not questionId:
            raise ValueError('A questionId is required.')
        query = session.query(Answer).filter_by(
            questionId=question
        )
        return query.all()

    @staticmethod
    def list_all_by_user(session: Session, user: str) -> List[Answer]:
        """Lists the `Answer`s assigned to a certain user.

        Args:
            - session (Session): The session object.
            - user (str): The user name string.

        Raises:
            - ValueError: If the user is missing.

        Returns:
            - List[Answer]: A list of `Answer` registers with the user roles.
        """
        if not user:
            raise ValueError('A user is required.')
        query = session.query(Answer).filter_by(
            user=user
        )
        return query.all()
