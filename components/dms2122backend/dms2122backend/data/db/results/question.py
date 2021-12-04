""" User class module.
"""

from typing import Dict
from sqlalchemy import Table, MetaData, Column, String  # type: ignore
#from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Float  # type: ignore
from dms2122backend.data.db.results.resultbase import ResultBase
#from dms2122auth.data.db.results.userrole import UserRole


class Question(ResultBase):
    """ Definition and storage of question ORM records.
    """

    def __init__(self, question:str,description:str,option1:str,option2:str,true_answer:str,selected_answer:str,correct_question_percentage:float,incorrect_question_percentage:float):
        """ Constructor method.

        Initializes a user record.

        Args:
            - question (str): A string with the question.
            - description (str): A string with the question's description.
            - option1 (str): A string with the first possible answer of the question.
            - option2 (str): A string with the second possible answer of the question.
            - true_answer (str): A string with the true answer of the question.
            - selected_answer (str): A string with the answer selected by the student. It must be None at the moment of its creation.
            - correct_question_percentage (float): A float with the percentage to be added in case of having the correct answer.
            - incorrect_question_percentage (float): A float with the percentage to be substracted in case of having the incorrect answer.
        """
        self.question: str = question
        self.desciption: str = description
        self.option1: str = option1
        self.option2: str = option2
        self.true_answer: str = true_answer
        self.selected_answer: str = selected_answer
        self.correct_question_percentage: float = correct_question_percentage
        self.incorrect_question_percentage: float = incorrect_question_percentage

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the table definition.

        Args:
            - metadata (MetaData): The database schema metadata
                        (used to gather the entities' definitions and mapping)

        Returns:
            - Table: A `Table` object with the table definition.
        """
        return Table(
            'users',
            metadata,
            Column('question', String(32), primary_key=True),
            Column('description', String(256), nullable=True),
            Column('opt1', String(32), nullable=False),
            Column('opt2', String(32), nullable=False),
            Column('true_answer', String(32), nullable=False),
            Column('selected_answer', String(32), nullable=True), #Se crean las preguntas con valores None. Es la selección del alumno a la pregunta
            Column('correct_question_percentage', Float(5), nullable=False),
            Column('incorrect_question_percentage', Float(5), nullable=False)
        )


