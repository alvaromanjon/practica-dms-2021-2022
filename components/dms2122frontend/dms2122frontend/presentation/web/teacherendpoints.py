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

        preguntas=[{
            "nombre_pregunta": "Radio del Sol", 
            "enunciado": "¿Cuál es el radio del Sol?",
            "opcion1": "696.340 km", 
            "opcion2": "432.182 km",
            "respuesta_correcta": 1,
            "porcentaje_correcta": 10,
            "porcentaje_incorrecta": 5},

            {"nombre_pregunta": "Distancia Tierra y Sol", 
            "enunciado": "¿A qué distancia está el Sol de la Tierra?",
            "opcion1": "28.371.823 km", 
            "opcion2": "149.597.870 km",
            "respuesta_correcta": 2,
            "porcentaje_correcta": 10,
            "porcentaje_incorrecta": 5},

            {"nombre_pregunta": "Constante G", 
            "enunciado": "¿Cuál es el valor de la constante de gravitación universal G?",
            "opcion1": "6,67*10^-11", 
            "opcion2": "9,8*10^-11",
            "respuesta_correcta": 1,
            "porcentaje_correcta": 10,
            "porcentaje_incorrecta": 5}
        ]     

        return render_template('/teacher/questions.html', name=name, roles=session['roles'], preguntas=preguntas)

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
        redirect_to = request.args.get('redirect_to', default='/teacher/questions')
        return render_template('/teacher/questions/add.html', name=name, roles=session['roles'],
                               redirect_to=redirect_to)

    @staticmethod
    def post_teacher_add_question(auth_service: AuthService) -> Union[Response, Text]:
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
            return redirect(url_for('get_teacher_add_question'))'''
        created_question = BackendService.create_question(BackendService,request.form['question'],
                                           request.form['description'],  
                                           request.form['opt1'],
                                           request.form['opt2'],
                                           request.form['true_answer'],
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
        redirect_to = request.args.get('redirect_to', default='/teacher/questions')
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
        redirect_to = request.args.get('redirect_to', default='/teacher/questions')
        return render_template('/teacher/questions/preview.html', name=name, roles=session['roles'],
                                redirect_to=redirect_to, nombre_pregunta=nombre_pregunta)

    @staticmethod
    def post_teacher_preview_question(auth_service: AuthService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.Teacher.name not in session['roles']:
            return redirect(url_for('get_home'))
        