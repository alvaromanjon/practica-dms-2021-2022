""" TeacherEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request, flash
from werkzeug.wrappers import Response
from dms2122common.data import Role
from dms2122frontend.data.rest import backendservice
from dms2122frontend.data.rest.authservice import AuthService
from dms2122frontend.data.rest.backendservice import BackendService
from .webauth import WebAuth
from .webquestion import WebQuestion
from .webanswer import WebAnswer

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
    def get_teacher_questions(auth_service: AuthService, backend_service: BackendService) -> Union[Response,Text]:
        """ Handles the GET requests to the questions teacher endpoint.
        Args:
            - auth_service (AuthService): The authentication service.
            - backend_service (BackendService): The backend service.
        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']

        return render_template('/teacher/questions.html', name=name, roles=session['roles'], 
                                questions=WebQuestion.list_questions(backend_service))

    @staticmethod
    def get_teacher_add_question(auth_service: AuthService) -> Union[Response, Text]:
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
        redirect_to = request.args.get('redirect_to', default='/questions')
        return render_template('/teacher/questions/add.html', name=name, roles=session['roles'],
                               redirect_to=redirect_to)

    @staticmethod
    def post_teacher_add_question(auth_service: AuthService, backend_service: BackendService) -> Union[Response, Text]:
        """ Handles the POST requests to the questions creation endpoint.

        Args:
            - auth_service (AuthService): The authentication service.
            - backend_service (BackendService): The backend service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))

        created_question = WebQuestion.create_question(backend_service, 
                                           request.form['question'],
                                           request.form['description'],  
                                           request.form['option1'],
                                           request.form['option2'],
                                           str(request.form['true_answer']),
                                           request.form['correct_answer_percentage'],
                                           request.form['incorrect_answer_percentage']
                                           )
        if not created_question:
            return redirect(url_for('get_teacher_add_question'))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_home')
        return redirect(redirect_to)

    @staticmethod
    def get_teacher_edit_question(auth_service: AuthService) ->Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        nombre_pregunta: str = str(request.args.get('nombre_pregunta'))
        redirect_to = request.args.get('redirect_to', default='/questions')
        return render_template('/teacher/questions/edit.html', name=name, roles=session['roles'],
                                redirect_to=redirect_to, nombre_pregunta=nombre_pregunta)

    @staticmethod
    def get_teacher_preview_question(auth_service: AuthService) ->Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        nombre_pregunta: str = str(request.args.get('nombre_pregunta'))
        redirect_to = request.args.get('redirect_to', default='/questions')
        return render_template('/teacher/questions/preview.html', name=name, roles=session['roles'],
                                redirect_to=redirect_to, nombre_pregunta=nombre_pregunta)

    @staticmethod
    def post_teacher_preview_question(auth_service: AuthService, backend_service: BackendService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))

        created_answer = WebAnswer.answer_question(backend_service, 
                                           request.form['user'],  
                                           int(request.form['questionId']),
                                           request.form['answer']
                                           )
        if not created_answer:
            return redirect(url_for('get_teacher_add_question'))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_home')
        return redirect(redirect_to)

    @staticmethod
    def post_teacher_preview_question(auth_service: AuthService, backend_service: BackendService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))

        created_answer = WebQuestion.edit_question(backend_service, 
                                           request.form['user'],  
                                           int(request.form['questionId']),
                                           request.form['answer']
                                           )
        if not created_answer:
            return redirect(url_for('get_teacher_add_question'))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_home')
        return redirect(redirect_to)



