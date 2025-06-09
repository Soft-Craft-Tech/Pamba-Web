import os
from dotenv import load_dotenv
from celery.schedules import crontab

class Config:
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('PAMBA_DB')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('EMAIL_ADDRESS')
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')


    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = 'Africa/Nairobi'
    CELERY_ENABLE_UTC = False
    CELERY_BEAT_SCHEDULE_FILENAME = 'celerybeat-schedule'
    CELERY_BEAT_SCHEDULE = {
        'resend-failed-notifications-every-30-minutes': {
            'task': 'CRON.celery_tasks.resend_failed_notifications',
            'schedule': crontab(minute='*/30'),
        },
    }