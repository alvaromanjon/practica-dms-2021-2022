""" QuestionServices class module.
"""

from typing import List, Dict, Optional
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.data.config import BackendConfiguration
from dms2122backend.data.db import Schema
from dms2122backend.data.db.results import Question
from dms2122backend.data.db.resultsets import Questions


class QuestionServices():
    """ Monostate class that provides high-level services to handle user-related use cases.
    """
    @staticmethod
    def get_question(question:str, description:str, option1:str, option2:str, true_answer:str,
                correct_question_percentage:float, incorrect_question_percentage:float, 
                schema: Schema) -> Optional[Question]:
        """Determines whether a user with the given credentials exists.

        Args:
            - question (str): A string with the question.
            - description (str): A string with the question's description.
            - option1 (str): A string with the first possible answer of the question.
            - option2 (str): A string with the second possible answer of the question.
            - true_answer (str): A string with the true answer of the question.
            - correct_question_percentage (float): A float with the percentage to be added in case of having the correct answer.
            - incorrect_question_percentage (float): A float with the percentage to be substracted in case of having the incorrect answer.
            - schema (Schema): A database handler where the users are mapped into.

        Returns:
            - question: Question that matches the parameters given.
            - None: If the question doesn't exists.
        """
        session: Session = schema.new_session()
        questionReturned = Questions.get_question(session, question, description, option1, option2, true_answer, 
                                        correct_question_percentage, incorrect_question_percentage)
        session.remove_session()
        return questionReturned

    @staticmethod
    def get_question_id(questionId: int, schema: Schema) -> Optional[Question]:
        """Determines whether a user with the given credentials exists.

        Args:
            - questionId (int): Question identifier.
            - schema (Schema): A database handler where the users are mapped into.

        Returns:
            - question: Question that matches the parameters given.
            - None: If the question doesn't exists.
        """
        session: Session = schema.new_session()
        question = Questions.get_question_id(session, questionId)
        session.remove_session()
        return question

    @staticmethod
    def list_questions(schema: Schema) -> List[Dict]:
        """Lists the existing questions.

        Args:
            - schema (Schema): A database handler where the users are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the users' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        questions: List[Question] = Questions.list_all(session)
        for question in questions:
            out.append({
                'questionName': question.question
            })
        schema.remove_session()
        return out

    @staticmethod
    def create_question(question:str, description:str, option1:str, option2:str, true_answer:str,
                        correct_question_percentage:float, incorrect_question_percentage:float, 
                        schema: Schema) -> Dict:
        """Creates a question.

        Args:
            - question (str): A string with the question.
            - description (str): A string with the question's description.
            - option1 (str): A string with the first possible answer of the question.
            - option2 (str): A string with the second possible answer of the question.
            - true_answer (str): A string with the true answer of the question.
            - correct_question_percentage (float): A float with the percentage to be added in case of having the correct answer.
            - incorrect_question_percentage (float): A float with the percentage to be substracted in case of having the incorrect answer.
            - schema (Schema): A database handler where the users are mapped into.

        Raises:
            - ValueError: If either the username or the password_hash is empty.
            - UserExistsError: If a user with the same username already exists.

        Returns:
            - Dict: A dictionary with the new user's data.
        """
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            new_question: Question = Questions.create(session, question, description, option1, option2, true_answer, 
                                        correct_question_percentage, incorrect_question_percentage)
            out['questionName'] = new_question.question
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out
