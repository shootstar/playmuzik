import os
CELERY_IMPORTS=("muzik")

CELERY_RESULT_BACKEND = "db+" + os.environ.get("DATABASE_URL")