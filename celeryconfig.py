import os
CELERY_IMPORTS=("muzik")

# CELERY_RESULT_BACKEND = "db+" + os.environ.get("DATABASE_URL")
BROKER_URL = os.environ.get('CLOUDAMQP_URL',"amqp://guest@localhost//")
