import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fpt_guide.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@fpt.edu.vn', 'admin123456')
    print('Superuser created!')
else:
    print('Already exists!')
