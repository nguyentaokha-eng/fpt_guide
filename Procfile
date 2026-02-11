release: python manage.py collectstatic --noinput
web: gunicorn fpt_guide.wsgi:application
