# BookStoreReleaseV1
# EN
This repository is my main Python/Django project. This web application is an online bookstore. The API part and frontend part are fully implemented in the application. In the future, a telegram client will be made.


To launch this project, you need:
1. Clone/download the git repository
2. Create a virtual environment for the project

    Install python version 3.9 or higher
		
  	python3 -venv /path/to/new/virtual/environment/
		
  	/path/to/new/virtual/environment/Scripts/activate.bat
		
  	In the project directory, enter pip install -r in the terminal requirements.txt
		
4. You need to connect the database for the project to work. If you don't need a special database, use in the file /BookStoreProject/settings.py and find the variable "databases" and insert

"
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': 'mydatabase',
}
}
"

5. After that, write "python manage.py makemigrations" and "python manage.py migrate" in the terminal
6. Write in the terminal "python manage.py createsuperuser" and create a superadmin with any values convenient for you
7. For normal use of the site, you need to go to the admin panel and create data of authors, categories and books themselves there
8. Also, for the site to work correctly, you need to find the mail settings in the /BookStoreProject/settings.py and fill email variables at the end of file.

Read more about smtp and django here https://bshoo.medium.com/how-to-send-emails-with-python-django-through-google-smtp-server-for-free-22ea6ea0fb8e

# To contact me, use telegram https://t.me/alwayswannaafly or discord LPFJ2#9620

# RU

Данный репозиторий является моим основным проектом по Python/Django. В приложении полностью разделен backend от frontend'а. Полностью сделан API приложения и фронт-клиент с использованием Vue.js. В будущем будет хочу сделать телеграмм-клиент.

Для запуска данного проекта вам необходимо: 
1. Клонировать/скачать гит репозиторий
2. Создать виртуальное окружение для работы проекта

a. Установите python версии 3.9 или выше

б. python3 -venv /path/to/new/virtual/environment/

с. /path/to/new/virtual/environment/Scripts/activate.bat

d. В директории проекта пропишите в терминале pip install -r requirements.txt

4. Вам необходимо подключить базу данных для работы проекта. Если вам не нужна особенная база данных используйте в файле /BookStoreProject/settings.py следующее.. найдите переменную "databases" и вставьте вместо нее


"
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': 'mydatabase',
}
}
"

5. После пропишите в терминале "python manage.py makemigrations" и "python manage.py migrate"
6. В терминале "python manage.py createsuperuser" и создайте суперадмина с любыми удобными для вас значениями
7. Для нормального пользования сайтом вам необходимо перейти в админскую панель и создать там данные авторов, категорий и самих книг
8. Также для корректной работы сайта вам необходимо найти настройки почты в файле /BookStoreProject/settings.py и заполнить переменные связанные с почтой

Подробнее про smtp и django читайте тут https://bshoo.medium.com/how-to-send-emails-with-python-django-through-google-smtp-server-for-free-22ea6ea0fb8e
# Для связи со мной используйте telegram https://t.me/alwayswannaafly или discord LPFJ2#9620
