""" Users class module.
"""

import hashlib
from typing import List, Optional
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2122backend.data.db.results import Question
from dms2122backend.data.db.exc import QuestionExistsError


class Questions():
    """ Class responsible of table-level questions operations.
    """
    @staticmethod
    def create(session: Session, question:str, description:str, option1:str, option2:str, true_answer:str,
                correct_question_percentage:float, incorrect_question_percentage:float) -> Question:
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
            - correct_question_percentage (float): The correct question percentage value.
            - incorrect_question_percentage (float): The incorrect question percentage value.

        Raises:
            - ValueError: If any of the fields are not found.
            - QuestionExistsError: If a question with the same name exists.

        Returns:
            - User: The created `User` result.
        """
        if not question or not option1 or not option2 or not true_answer or not correct_question_percentage or not incorrect_question_percentage:
            raise ValueError('ERROR. The following fields are required:\n-Question\n-Description (optional field) \n-First option\n-Second option\n-True answer\n-Correct question percentage\n-Incorrect question percentage')
        try:
            new_question = Question(question, description, option1, option2, 
                                    true_answer, correct_question_percentage, incorrect_question_percentage)
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
    def get_question(session: Session, question: str, description:str, option1:str, option2:str, true_answer:str, 
                correct_question_percentage:float, incorrect_question_percentage:float) -> Optional[Question]:
        """ Returns a question (if exists).

        Args:
            - session (Session): The session object.
            - question (str): A string with the question.
            - description (str): A string with the question's description.
            - option1 (str): A string with the first possible answer of the question.
            - option2 (str): A string with the second possible answer of the question.
            - true_answer (str): A string with the true answer of the question.
            - correct_question_percentage (float): A float with the percentage to be added in case of having the correct answer.
            - incorrect_question_percentage (float): A float with the percentage to be substracted in case of having the incorrect answer.

        Returns:
            - question: Question that matches the parameters given.
            - None: If the question doesn't exists.
        """
        try:
            query = session.query(Question).filter_by(question=question, description=description, 
                                                    option1=option1, option2=option2, true_answer=true_answer, 
                                                    correct_question_percentage=correct_question_percentage,
                                                    incorrect_question_percentage=incorrect_question_percentage)
            query.one()
        except NoResultFound:
            return None
        return Question
    
    @staticmethod
    def get_question_by_id(session: Session, questionId: int) -> Optional[Question]:
        """ Returns a question (if exists).

        Args:
            - session (Session): The session object.
            - questionId (int): Question identifier.
            
        Returns:
            - question: Question that matches the parameters given.
            - None: If the question doesn't exists.
        """
        try:
            query = session.query(Question).filter_by(questionId=questionId)
            query.one()
        except NoResultFound:
            return None
        return Question
