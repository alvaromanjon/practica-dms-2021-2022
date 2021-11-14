""" TeacherEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request, flash
from werkzeug.wrappers import Response
from dms2122common.data import Role
from dms2122frontend.data.rest.authservice import AuthService
from .webauth import WebAuth
from .webuser import WebUser

class TeacherEndpoints():
    """ Monostate class responsible of handing the teacher web endpoint requests.
    """
    @staticmethod
    def get_teacher(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the teacher root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('teacher.html', name=name, roles=session['roles'])

    @staticmethod
    def get_teacher_questions(auth_service: AuthService) ->Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('/teacher/questions.html', name=name, roles=session['roles'])

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

    @staticmethod
    def add_question(auth_service: AuthService) -> Union[Response, Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        #if Role.Teacher.name not in session['roles']:
        #    return redirect(url_for('get_home'))
        name = session['user']
        return render_template('/teacher/questions/add.html', name=name, roles=session['roles'])

    @staticmethod
    def get_add_question(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the questions creation endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        redirect_to = request.args.get('redirect_to', default='/teacher/questions')
        return render_template('/teacher/questions/add.html', name=name, roles=session['roles'],
                               redirect_to=redirect_to
                               )

    @staticmethod
    def post_add_question(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the POST requests to the questions creation endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        '''if request.form['password'] != request.form['confirmpassword']:
            flash('Password confirmation mismatch', 'error')
            return redirect(url_for('get_add_question'))'''
        created_question = WebUser.create_question(auth_service,
                                           request.form['question'], 
                                           request.form['opt1'],
                                           request.form['opt2'],
                                           request.form['true_answer']
                                           )
        if not created_question:
            return redirect(url_for('get_add_question'))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_home')
        return redirect(redirect_to)

    @staticmethod
    def edit_question(auth_service: AuthService) -> Union[Response, Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('/questions/edit.html', name=name, roles=session['roles'])