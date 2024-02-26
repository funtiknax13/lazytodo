# Менеджер задач на Django

Для запуска необходимо создать файл `.env` в папке проекта и задать следующие переменные:
- SECRET_KEY=
- DEBUG=
Данные почтового сервера:
- EMAIL_HOST_USER=
- EMAIL_HOST_PASSWORD=


Для запуска:
```
установить виртуальное окружение:
   python -m venv venv
установить библиотеки из файла requirements.txt:
   pip install -r requirements.txt
провести миграции БД
    python manage.py makemigrations
    python manage.py migrate
запустить приложение
    python manage.py runserver
```
Работа с приложением:
```
Создание суперпользователя:
   python manage.py createsuperuser
```
