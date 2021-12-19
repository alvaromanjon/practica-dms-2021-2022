""" QuestionServices class module.
"""

from typing import List, Dict, Optional
from sqlalchemy.orm.session import Session  # type: ignore
from dms2122backend.data.config import BackendConfiguration
from dms2122backend.data.db import Schema
from dms2122backend.data.db.results import Question
from dms2122backend.data.db.resultsets import Questions


class QuestionServices():
    """ Monostate class that provides high-level services to handle question-related use cases.
    """

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
            - ex: If the question can't be created.

        Returns:
            - Dict: A dictionary with the new question's data.
        """
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            newQuestion: Question = Questions.create(session, question, description, option1, option2, true_answer, 
                                        correct_question_percentage, incorrect_question_percentage)
            out['questionId'] = newQuestion.questionId #type: ignore
            out['question'] = newQuestion.question
            out['description'] = newQuestion.description
            out['option1'] = newQuestion.option1
            out['option2'] = newQuestion.option2
            out['true_answer'] = newQuestion.true_answer
            out['correct_question_percentage'] = newQuestion.correct_question_percentage
            out['incorrect_question_percentage'] = newQuestion.incorrect_question_percentage
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def list_questions(schema: Schema) -> List[Dict]:
        """Lists the existing questions.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the questions' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        questionsReturned: List[Question] = Questions.list_all(session)
        for eachQuestion in questionsReturned:
            out.append({
                'questionId': eachQuestion.questionId, #type: ignore
                'question': eachQuestion.question,
                'description': eachQuestion.description,
                'option1': eachQuestion.option1,
                'option2': eachQuestion.option2,
                'true_answer': eachQuestion.true_answer,
                'correct_question_percentage': eachQuestion.correct_question_percentage,
                'incorrect_question_percentage': eachQuestion.incorrect_question_percentage
            })
        schema.remove_session()
        return out

    @staticmethod
    def get_question_id(questionId: int, schema: Schema) -> Dict:
        """Returns a question (if exists).

        Args:
            - questionId (int): Question identifier.
            - schema (Schema): A database handler where the questions are mapped into.

        Raises:
            - ex: If the question can't be created.

        Returns:
            - out: Dictionary with all the question data.
            - None: If the question doesn't exists.
        """
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            questionReturned = Questions.get_question_id(session, questionId)
            if questionReturned is not None:
                out['questionId'] = questionReturned.questionId #type: ignore
                out['question'] = questionReturned.question
                out['description'] = questionReturned.description
                out['option1'] = questionReturned.option1
                out['option2'] = questionReturned.option2
                out['true_answer'] = questionReturned.true_answer
                out['correct_question_percentage'] = questionReturned.correct_question_percentage
                out['incorrect_question_percentage'] = questionReturned.incorrect_question_percentage
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def edit_question(questionId: int, question:str, description:str, option1:str, option2:str, true_answer:str,
                        correct_question_percentage:float, incorrect_question_percentage:float, 
                        schema: Schema) -> Dict:
        """Edits a question.

        Args:
            - questionId (int): Question identifier.
            - question (str): A string with the question.
            - description (str): A string with the question's description.
            - option1 (str): A string with the first possible answer of the question.
            - option2 (str): A string with the second possible answer of the question.
            - true_answer (str): A string with the true answer of the question.
            - correct_question_percentage (float): A float with the percentage to be added in case of having the correct answer.
            - incorrect_question_percentage (float): A float with the percentage to be substracted in case of having the incorrect answer.
            - schema (Schema): A database handler where the users are mapped into.

        Raises:
            - ex: If the question can't be edited.

        Returns:
            - Dict: A dictionary with the edited question's data.
        """
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            editedQuestion: Question = Questions.edit(session, questionId, question, description, option1, option2, true_answer, 
                                        correct_question_percentage, incorrect_question_percentage)
            out['questionId'] = editedQuestion.questionId # type: ignore
            out['question'] = editedQuestion.question
            out['description'] = editedQuestion.description
            out['option1'] = editedQuestion.option1
            out['option2'] = editedQuestion.option2
            out['true_answer'] = editedQuestion.true_answer
            out['correct_question_percentage'] = editedQuestion.correct_question_percentage
            out['incorrect_question_percentage'] = editedQuestion.incorrect_question_percentage
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out