echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.count() == 0 and User.objects.create_superuser('admin@ctagroup.org', 'password')" | python manage.py shell
python manage.py collectstatic --no-input
python manage.py migrate --no-input
