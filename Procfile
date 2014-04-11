web: gunicorn -b 0.0.0.0:$PORT muzik:app
worker: celery -A muzik:celery worker --loglevel=info

