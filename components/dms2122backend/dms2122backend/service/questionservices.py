""" UserServices class module.
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
            - cfg (AuthConfiguration): The application configuration.

        Returns:
            - bool: `True` if the given user exists. `False` otherwise.
        """
        session: Session = schema.new_session()
        password_hash: str = Users.hash_password(
            password, suffix=username, salt=salt)
        session: Session = schema.new_session()
        user_exists: bool = Users.user_exists(session, username, password_hash)
        schema.remove_session()
        return user_exists

    @staticmethod
    def list_users(schema: Schema) -> List[Dict]:
        """Lists the existing users.

        Args:
            - schema (Schema): A database handler where the users are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the users' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        users: List[User] = Users.list_all(session)
        for user in users:
            out.append({
                'username': user.username
            })
        schema.remove_session()
        return out

    @staticmethod
    def create_user(username: str, password: str, schema: Schema, cfg: BackendConfiguration) -> Dict:
        """Creates a user.

        Args:
            - username (str): The new user's name.
            - password (str): The new user's password.
            - schema (Schema): A database handler where the users are mapped into.
            - cfg (AuthConfiguration): The application configuration.

        Raises:
            - ValueError: If either the username or the password_hash is empty.
            - UserExistsError: If a user with the same username already exists.

        Returns:
            - Dict: A dictionary with the new user's data.
        """
        salt: str = cfg.get_password_salt()
        password_hash: str = Users.hash_password(
            password, suffix=username, salt=salt)
        session: Session = schema.new_session()
        out: Dict = {}
        try:
            new_user: User = Users.create(session, username, password_hash)
            out['username'] = new_user.username
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out
