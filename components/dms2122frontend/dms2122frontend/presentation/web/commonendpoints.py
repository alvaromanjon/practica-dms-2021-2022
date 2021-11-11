""" CommonEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template
from werkzeug.wrappers import Response
from dms2122frontend.data.rest.authservice import AuthService
from .webauth import WebAuth


class CommonEndpoints():
    """ Monostate class responsible of handling the common web endpoint requests.
    """
    @staticmethod
    def get_home(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the home endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        name = session['user']
        return render_template('home.html', name=name, roles=session['roles'])

    @staticmethod
    def get_questions(auth_service: AuthService) ->Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        name = session['user']
        return render_template('/questions/questions.html', name=name, roles=session['roles'])

    @staticmethod
    def do_the_test(auth_service: AuthService) ->Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        name = session['user']
        return render_template('/questions/do_the_test.html', name=name, roles=session['roles'])

    @staticmethod
    def see_answers(auth_service: AuthService) ->Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        name = session['user']
        return render_template('/questions/answers.html', name=name, roles=session['roles'])
