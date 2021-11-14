![pylint score](https://github.com/alvaromanjon/practica-dms-2021-2022/workflows/pylint%20score/badge.svg)
![mypy typechecking](https://github.com/alvaromanjon/practica-dms-2021-2022/workflows/mypy%20typechecking/badge.svg)

# DMS course project codebase, academic year 2021-2022

The goal of this project is to implement a basic online evaluation appliance deployed across several interconnected services.
# Authors
 * [María Alonso Peláez](https://github.com/map10100)
 * [Álvaro Manjón Vara](https://github.com/alvaromanjon)
 * [Pablo Ahíta del Barrio](https://github.com/pabloahita)

## Components

The source code of the components is available under the `components` direcotry.

### Services

The services comprising the appliance are:

#### `dms2122auth`

This is the authentication service. It provides the user credentials, sessions and rights functionalities of the application.

See the `README.md` file for further details on the service.

#### `dms2122backend`

This service provides the evaluation logic (definition of questions, grading, etc.)

See the `README.md` file for further details on the service.

#### `dms2122frontend`

A frontend web service that allows to interact with the other services through a web browser.

See the `README.md` file for further details on the application.

### Libraries

These are auxiliar components shared by several services.

#### `dms2122core`

The shared core functionalities.

See the `README.md` file for further details on the component.

## Docker

The application comes with a pre-configured Docker setup to help with the development and testing (though it can be used as a base for more complex deployments).

To run the application using Docker Compose:

```bash
docker-compose -f docker/config/dev.yml up -d
```

When run for the first time, the required Docker images will be built. Should images be rebuilt, do it with:

```bash
docker-compose -f docker/config/dev.yml build
```

To stop and remove the containers:

```bash
docker-compose -f docker/config/dev.yml rm -sfv
```

By default data will not be persisted across executions. The configuration file `docker/config/dev.yml` can be edited to mount persistent volumes and use them for the persistent data.

To see the output of a container:

```bash
docker logs CONTAINER_NAME
# To keep printing the output as its streamed until interrupted with Ctrl+C:
# docker logs CONTAINER_NAME -f
```

To enter a running service as another subprocess to operate inside through a terminal:

```bash
docker exec -it CONTAINER_NAME /bin/bash
```

To see the status of the different containers:

```bash
docker container ps -a
```

## Helper scripts

The directory `scripts` contain several helper scripts.

- `verify-style.sh`: Runs linting (using pylint) on the components' code. This is used to verify a basic code quality. On GitHub, this CI pass will fail if the overall score falls below 7.00.
- `verify-type-correctness.sh`: Runs mypy to assess the type correctness in the components' code. It is used by GitHub to verify that no typing rules are broken in a commit.
- `verify-commit.sh`: Runs some validations before committing a changeset. Right now enforces type correctness (using `verify-type-correctness.sh`). Can be used as a Git hook to avoid committing a breaking change:
  Append at the end of `.git/hooks/pre-commit`:

  ```bash
  scripts/verify-commit.sh
  ```

## GitHub workflows and badges

This project includes some workflows configured in `.github/workflows`. They will generate the badges seen at the top of this document, so do not forget to update the URLs in this README file if the project is forked!

# Manual de instalación 
Para la instalación el primer paso que vamos a realizar es descargarnos la maquina virtual, donde tendremos ya todos los materiales y programas necesarios, desde github con el comando:
```bash
wget -qL https://gist.github.com/Kencho/b3829dd99c2c41c9f7a0c854b41dcaf4/raw/bootstrap.sh -O /dev/stdout | sudo bash -
```
Este script esta pensado para que funcione con la distribución Ubuntu 20.04.1

Esta es una de las opciones para tener el entorno preparado, en caso de querer hacerlo paso a paso lo primero que debemos hacer es descargarnos una máquina virtual que contenga Ubuntu.20.04.1, ademas también debemos tener descargado Visual Studio. A continuación debemos instalar Docker y docker compose, para ello vamos a serguir los siguientes pasos:
### Añadir la clave GPG de Docker:
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt-key fingerprint 0EBFCD88
```
### Añadir repositorio de Docker
```bash
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```
### Instalar Docker
```bash
apt update
apt install -y docker-ce docker-ce-cli containerd.io
```
### Instalar Docker Compose
```bash
curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```
### Añadir el usuario al grupo docker
```bash
usermod -a -G docker "${USER_NAME}"
```
# Manual de uso 
Una vez realizados los pasos de instalación, vamos a ver como se utiliza la aplicación.

### Comando de ejecución
Hemos creado un comando llamado `ejecutar.sh` que se encarga de automatizar el proceso de parada, borrado de los contenedores y re-ejecución de los mismos, lo cual es muy útil a la hora de hacer cambios, ya que hay que volver a ejecutar todo para que se apliquen. Deberemos de darle permisos de ejecución la primera vez que lo usemos con `chmod +x ejecutar.sh`, y después para ejecutarlo usaremos el comando `./ejecutar.sh`.
## Login
Lo primero que nos aparece es la primera ventana que es la de Login.
En este apartado nos aparecen los campos de usuario y contraseña que el usuario debe instroducir para acceder a la aplicación.
![login](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/5afd0384b803009a0e7b883ddd96b233aac535d8/imagenes/login.png)
Esta aplicación cuenta con tres tipos de usuario: 
- Admin: Este tipo de usuario cuenta con todos los permisos y a partir de el se podrán crear nuevos usuarios dandoles los permisos correspondientes (usuario: admin, Contraseña: admin)
- Teacher: El usuario con el rol de profesor tiene los permisos necesarios para crear y editar preguntas asi como visualizarlas, podrá ver cuantas veces se ha seleccionado cada respuesta y obtener un promedio de ellas y finalmente ver el progreso de los alumnos.
- Student: Este usuario podrá ver las preguntas que tiene pendientes y contestarlas. Tambien podrá ver su progeso en la plataforma.

## Admin
Si accedemos como admin nos aparece la ventana "Panel de administración".
![admin1](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/main/imagenes/panel%20de%20administraci%C3%B3n.png)
donde tenemos la opción gestión de usuarios,en este apartado nos sale un formulario de registro en la plataforma donde debemos introducir el usuario, la contraseña y verificar la contraseña. 
![admin2](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/main/imagenes/administraci%C3%B3n%20usuarios.png)
![admin3](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/main/imagenes/crear%20usuario.png)
Si en la ventana de administrar los usuarios le damos a editar podemos elegir cual de los tres roles va a tener el usuario.
![admin4](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/5afd0384b803009a0e7b883ddd96b233aac535d8/imagenes/rol.png)
## Teacher 
Si el usuario que accede a la web tiene el rol de profesor, le aparecerá la siguiente pantalla:
![teacher1](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/main/imagenes/panel%20teacher.png)
accedemos y nos aparecera una pantalla en la que podemos visualizar las preguntas, tenemos el botón editar para poder modificalas, previsualizarlas y un botón añadir preguntas.

![teacher2](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/main/imagenes/Gestion%20de%20preguntas%20teacher.png)
si queremos añadir una nueva pregunta, se nos mostrara una pantalla en la que tendremos que rellenar los campos: titulo, enunciado, opciones, que opción es la correcta y los valores en caso de que la pregunta sea correcta o incorrecta.
![teacher3](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/main/imagenes/a%C3%B1adir%20pregunta.png)
si queremos modificar una pregunta, solo debemos pulsar el botón modificar que se encuentra al lado de ella, nos aparecerá una ventana con los mismo campos que en el apartado de crear pregunta y modificaremos lo que sea necesario.
![teacher4](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/main/imagenes/editar%20pregunta.png)
Por último, si queremos previsualizar una pregunta, de la misma forma que lo haría un estudiante, en la pantalla le aparece el titulo, enunciado y las opciones.
![teacher5](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/main/imagenes/previsuaizar%20teacher.png)
## Student 
Si accedemos a la web con permiso de estudiante solo podremos ver las preguntas y responderlas.
![Student](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/main/imagenes/administracion%20student.png)
Primero nos aparece la pantalla con las preguntas que tenemos dispo0nible y vemos el nombre y enunciado.
![Student2](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/main/imagenes/preguntas%20student.png)
Si le damos al boton responder nos da la opción de responder las preguntas.
![Student3](https://github.com/alvaromanjon/practica-dms-2021-2022/blob/main/imagenes/preguntas%20student.png)
# Arquitectura y diseño del frontend
