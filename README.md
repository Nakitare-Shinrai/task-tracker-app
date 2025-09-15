# Setting Up a REST API Service for Task Tracker
#### A step-by-step guide
1. In your terminal create a virtual environment by running the commands `mkdir env` then `python3 -m venv env`
2. To start your virtual environment run the command `source env/bin/activate` .To stop the environment run `deactivate` command
3. Install dependancies using this command in the root directory of the project `pip install -r requirements.txt`
4. Move to the project directory using the command `cd task-tracker`
5. To configure your database go to the `settings.py` file and edit the properties below, bearing in mind postgres servers and client is installed on your machine 

DATABASES = {
    'default': {
        'NAME': 'your_DB_name',
        'HOST': 'localhost',
        'USER': 'Your_username',
        'PASSWORD': 'Your_password',
        'PORT': '5432',
    }
}

6. Run `python manage.py makemigrations` to initialize migrations then run `python manage.py migrate` to migrate models to your database
7. Run `python manage.py createsuperuser` to craete credentials for user placement orders.
8. To start you application run the command `python manage.py runserver`
