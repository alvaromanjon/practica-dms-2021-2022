""" StudentEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request 
from werkzeug.wrappers import Response
from dms2122common.data import Role
from dms2122frontend.data.rest.authservice import AuthService
from dms2122frontend.data.rest.backendservice import BackendService
from .webauth import WebAuth
from .webquestion import WebQuestion

class StudentEndpoints():
    """ Monostate class responsible of handling the student web endpoint requests.
    """
    @staticmethod
    def get_student(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the student root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Student.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        return render_template('student.html', name=name, roles=session['roles'])
    
    @staticmethod
    def get_student_questions(auth_service: AuthService, backend_service: BackendService) ->Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Student.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']

        return render_template('/student/questions.html', name=name, roles=session['roles'], preguntas=WebQuestion.list_questions(backend_service))
    
    @staticmethod
    def get_student_preview_question(auth_service: AuthService) ->Union[Response,Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Student.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']
        nombre_pregunta: str = str(request.args.get('nombre_pregunta'))
        redirect_to = request.args.get('redirect_to', default='/student/questions')
        return render_template('/student/questions/answer.html', name=name, roles=session['roles'],
                                redirect_to=redirect_to, nombre_pregunta=nombre_pregunta)

    @staticmethod
    def post_student_preview_question(auth_service: AuthService, backend_service: BackendService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))

        created_answer = WebQuestion.answer_question(backend_service, 
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


