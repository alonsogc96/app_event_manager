# Proyecto "Gestor de Eventos" en Django Rest Framework

Este es un proyecto para gestionar eventos utilizando Django y Django Rest Framework (DRF) para la creación de una API RESTful. El proyecto está configurado para ser desplegado y ejecutado localmente en un entorno de desarrollo.

## Requisitos

Antes de comenzar, asegurarse de tener los siguientes requisitos instalados en tu sistema:

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Postgresql
- Git

## Instalación

### 1. Clonar el repositorio

Clonar el proyecto con el siguiente comando:

```bash
git clone https://github.com/alonsogc96/app_event_manager.git
cd app_event_manager
```

### 2. Crear un entorno virtual

Es recomendable crear un entorno virtual para gestionar las dependencias de tu proyecto. Se puede crear un entorno virtual utilizando `venv`:

```bash
python -m venv venv
```

Luego, activar el entorno virtual:

- En Linux/macOS:

  ```bash
  source venv/bin/activate
  ```

- En Windows:

  ```bash
  venv\Scripts\activate
  ```

### 3. Instalar las dependencias

Una vez dentro del entorno virtual, instalar las dependencias necesarias con pip:

```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos

Conectarse al servidor local de Postgresql:

```bash
psql -U postgres
```

Una vez conectado, crear la base de datos usando el comando CREATE DATABASE:

```bash
CREATE DATABASE app_events
```

### 5. Generar un secret_key

Ejecutar el siguiente comando para generar el secret_key:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 6. Configurar las variables de entorno

Crear un archivo .env y configurarlo:

```bash
cp .env.example .env
```

Cambiar la configuración de la BD y del secrey_key según tus credenciales.

### 7. Realizar las migraciones

Django utiliza migraciones para crear la estructura de la base de datos. Correr el siguiente comando para aplicar las migraciones:

```bash
python manage.py migrate
```

### 8. Crear un superusuario

Para acceder al panel de administración de Django, crear un superusuario:

```bash
python manage.py createsuperuser
```

Escribir un nombre de usuario, correo electrónico y contraseña.

### 9. Ejecutar las pruebas unitarias (opcional)

Para realizar las pruebas unitarias ejecutar el siguiente comando:

```bash
python manage.py test
```

### 10. Ejecutar el servidor de desarrollo

Iniciar el servidor de desarrollo de Django con el siguiente comando:

```bash
python manage.py runserver
```

Por defecto, el servidor se ejecutará en `http://localhost:8000/`.

### 11. Acceder a la API

Una vez que el servidor esté en funcionamiento, puedes probar la API con Swagger en:

```
http://localhost:8000/docs/
```

También se puede revisar la documentación de Redoc accediendo a:

```
http://localhost:8000/redoc/
```

Desde la API, se puede crear usuarios administradores y regulares.

### 12. Acceder al panel de administración (opcional)

Acceder al panel de administración de Django en:

```
http://localhost:8000/admin/
```

Inicia sesión con las credenciales del superusuario que creaste.

## Roles

- **Administrador**: Gestión total de usuarios y eventos.
- **Usuario regular**: Puede ver todos los eventos y registrarse en uno. Además puede obtener una lista con los eventos a los que se ha registrado.

## Tecnologías usadas

- **Django**: Framework para aplicaciones web en Python.
- **Django Rest Framework (DRF)**: Extensión de Django para crear APIs RESTful.
- **PostgreSQL**: Bases de datos utilizadas para almacenar datos.



## Despliegue en AWS Elastic Beanstalk (Opcional)

Para desplegar este proyecto en **AWS Elastic Beanstalk**, seguir los pasos a continuación:

### 1. Instalar la CLI de AWS Elastic Beanstalk

Si aún no tienes instalada la CLI de Elastic Beanstalk, puedes hacerlo siguiendo estos pasos:

1.1 **Configurar AWS CLI**: Si aún no has configurado tu AWS CLI, hazlo con el siguiente comando y sigue las instrucciones para ingresar tus credenciales de AWS:

```
pip install awscli
aws configure
```

1.2 **Instalar la CLI de AWS EB**: 

```
pip install awsebcli
```

### 2. Iniciar el repositorio de la CLI de EB 


```
eb init -p python-3.9 django-app
```

### 3. Crear un entorno e implementar la aplicación en él con eb create. 

```
eb create django-env
```

Cuando finalice el proceso de creación del entorno, visualizar el estado con:

```
eb status django-env
```

### 4. Configurar las variables de entorno. 

```
eb setenv SECRET_KEY='YOUR_SECRET_KEY' DATABASE_URL='YOUR_DB_URL'
```

Reemplazar por las credenciales correspondientes. Para la base de datos, puede crearse una gratuita en [Tembo](https://tembo.io/). 

### 5. Desplegar la aplicación. 

```
eb deploy
```

### 6. Abrir la aplicación. 

```
eb open
```

Para más detalles sobre el despliegue puede consultar la documentación oficial en [AWS](https://docs.aws.amazon.com/es_es/elasticbeanstalk/latest/dg/create-deploy-python-django.html)

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.