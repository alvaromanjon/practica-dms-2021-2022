""" User class module.
"""

from typing import Dict
from sqlalchemy import Table, MetaData, Column, String, relationship  # type: ignore
from sqlalchemy.sql.sqltypes import Float  # type: ignore
from dms2122backend.data.db.results.resultbase import ResultBase
from dms2122backend.data.db.results.answer import Answer


class Question(ResultBase):
    """ Definition and storage of question ORM records.
    """

    def __init__(self, question:str, description:str, option1:str, option2:str, true_answer:str, 
                correct_question_percentage:float, incorrect_question_percentage:float):
        """ Constructor method.

        Initializes a user record.

        Args:
            - question (str): A string with the question.
            - description (str): A string with the question's description.
            - option1 (str): A string with the first possible answer of the question.
            - option2 (str): A string with the second possible answer of the question.
            - true_answer (str): A string with the true answer of the question.
            - correct_question_percentage (float): A float with the percentage to be added in case of having the correct answer.
            - incorrect_question_percentage (float): A float with the percentage to be substracted in case of having the incorrect answer.
        """
        self.question: str = question
        self.desciption: str = description
        self.option1: str = option1
        self.option2: str = option2
        self.true_answer: str = true_answer
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
            'questions',
            metadata,
            Column('question', String(32), primary_key=True),
            Column('description', String(256), nullable=True),
            Column('opt1', String(32), nullable=False),
            Column('opt2', String(32), nullable=False),
            Column('true_answer', String(32), nullable=False),
            Column('correct_question_percentage', Float(5), nullable=False),
            Column('incorrect_question_percentage', Float(5), nullable=False)
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        """ Gets the mapping properties dictionary.

        Returns:
            - Dict: A dictionary with the mapping properties.
        """
        return {
            'questions': relationship(Answer, backref='question')
        }
