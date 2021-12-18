""" StudentEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request 
from werkzeug.wrappers import Response
from dms2122common.data import Role
from dms2122frontend.data.rest.authservice import AuthService
from dms2122frontend.data.rest.backendservice import BackendService
from .webauth import WebAuth
from .webuser import WebUser

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
        #preguntas=[{
        #    "nombre_pregunta": "Radio del Sol", 
        #    "enunciado": "¿Cuál es el radio del Sol?",
        #    "opcion1": "696.340 km", 
        #    "opcion2": "432.182 km",
        #    "respuesta_correcta": 1,
        #    "porcentaje_correcta": 10,
        #    "porcentaje_incorrecta": 5},

        #    {"nombre_pregunta": "Distancia Tierra y Sol", 
        #    "enunciado": "¿A qué distancia está el Sol de la Tierra?",
        #    "opcion1": "28.371.823 km", 
        #    "opcion2": "149.597.870 km",
        #    "respuesta_correcta": 2,
        #    "porcentaje_correcta": 10,
        #    "porcentaje_incorrecta": 5},

        #    {"nombre_pregunta": "Constante G", 
        #    "enunciado": "¿Cuál es el valor de la constante de gravitación universal G?",
        #    "opcion1": "6,67*10^-11", 
        #    "opcion2": "9,8*10^-11",
        #    "respuesta_correcta": 1,
        #    "porcentaje_correcta": 10,
        #    "porcentaje_incorrecta": 5}
        #]
        return render_template('/student/questions.html', name=name, roles=session['roles'], preguntas=WebUser.list_questions(backend_service))
    
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