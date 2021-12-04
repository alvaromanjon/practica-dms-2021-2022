""" Users class module.
"""

import hashlib
from typing import List
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2122backend.data.db.results import Question
from dms2122backend.data.db.exc import QuestionExistsError


class Questions():
    """ Class responsible of table-level questions operations.
    """
    @staticmethod
    def create(session: Session, question:str,description:str,option1:str,option2:str,true_answer:str,selected_answer:str,correct_question_percentage:float,incorrect_question_percentage:float) -> Question:
        """ Creates a new user record.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - question (str): The question string.
            - description (str): The description string.
            - option1 (str): The first option string.
            - option2 (str): The second option string.
            - true_answer (str): The true answer string.
            - selected_answer (str): The selected answer string.
            - correct_question_percentage (float): The correct question percentage value.
            - incorrect_question_percentage (float): The incorrect question percentage value.

        Raises:
            - ValueError: If either the username or the password_hash is empty.
            - UserExistsError: If a user with the same username already exists.

        Returns:
            - User: The created `User` result.
        """
        if not question or not option1 or not option2 or not true_answer or not correct_question_percentage or not incorrect_question_percentage:
            raise ValueError('ERROR. The following fields are requiered:\n-Question\n-Description (optional field) \n-First option\n-Second option\n-True answer\n-Correct question percentage\n-Incorrect question percentage')
        try:
            new_question = Question(question,description,option1,option2,true_answer,selected_answer,correct_question_percentage,incorrect_question_percentage)
            session.add(new_question)
            session.commit()
            return new_question
        except IntegrityError as ex:
            raise QuestionExistsError(
                'The question ' + question + ' already exists.'
                ) from ex

    @staticmethod
    def list_all(session: Session) -> List[Question]:
        """Lists every question.

        Args:
            - session (Session): The session object.

        Returns:
            - List[User]: A list of `User` registers.
        """
        query = session.query(Question)
        return query.all()

    @staticmethod
    def question_exists(session: Session, question: str) -> bool:
        """ Determines whether a user exists or not.

        Args:
            - session (Session): The session object.
            - question (str): The question string.

        Returns:
            - bool: `True` if a question with the given credential exists; `False` otherwise.
        """
        try:
            query = session.query(Question).filter_by(question=question)
            query.one()
        except NoResultFound:
            return False
        return True
