web: bash -lc "python manage.py migrate --noinput && gunicorn expense_tracker.wsgi:application --workers 3 --bind 0.0.0.0:$PORT"
