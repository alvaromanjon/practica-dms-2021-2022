""" Answer class module.
"""

from sqlalchemy import Table, MetaData, Column, ForeignKey, String, Integer  # type: ignore
from dms2122backend.data.db.results.resultbase import ResultBase


class Answer(ResultBase):
    """ Definition and storage of user role ORM records.
    """

    def __init__(self, user: str, answer: str, questionId: int):
        """ Constructor method.

        Initializes a user role record.

        Args:
            - user (str): A string with the user.
            - answer (str): A string with the selected answer by the user.
            - questionId (int): An identifier for the question answered.
        """
        self.user: str = user
        self.answer: str = answer
        self.questionId: int = questionId

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
            'answers',
            metadata,
            Column('user', String(32),
                   primary_key=True),
            Column('answer', String(32), nullable=False),
            Column('questionId', Integer,
                    ForeignKey('questions.questionId'), primary_key=True)
        )