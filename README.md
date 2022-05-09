**Word-Segmentation system**
-
1.Clone project

    git clone https://github.com/gamepalot/word-segmentation.git


2.Setting Environment

    pip install -r requirements.txt


3.Create New Database in **PostgreSQL**


4.Config Database in 

> wordseg/setting.py

    DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'NAME': 'databasename',
			'USER': 'postgres',
			'PASSWORD': '******',
			'HOST': 'localhost',
			}
		}


5.Migrate Project with Database

 1. `python manage.py makemigrations wordseg_app`
 2. `python manage.py migrate`


6.Create Super User for Login

    python manage.py createsuperuser


7.Run Project

	python manage.py runserver
   **or**

    python manage.py runserver host:port


