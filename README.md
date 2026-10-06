# Факультет природничих наук НаУКМА

Обидві частини лабораторної: Django 5.2, SQLite, звичайні HTML-шаблони та CSS.
Python 3.10 або новіший. Початковий контент завантажується міграціями.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install 'Django==5.2.18'
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/ · Адмінка: http://127.0.0.1:8000/admin/
Обліковий запис адміністратора створюється командою вище; готових паролів немає.
Налаштування призначені для локальної лабораторної роботи.

```sh
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
python manage.py migrate faculty zero
python manage.py migrate
```

`zero` видаляє весь контент застосунку `faculty`; наступний `migrate` відновлює
початкові дані. Подробиці, джерела й відповіді — у [ANSWERS.md](ANSWERS.md).
Тест виконується в окремій базі та перевіряє сторінки й міграції в обидва боки.

У `main` знаходиться початковий каркас `django-admin startproject`.
Гілка `lab/faculty-exchange` містить обидві частини роботи; міграції входять до PR,
оскільки реалізують завдання та потрібні для відтворення бази.
