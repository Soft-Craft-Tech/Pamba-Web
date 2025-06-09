from celery import Celery
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate
from API.config import Config

db = SQLAlchemy()
mail = Mail()
bcrypt = Bcrypt()
migrate = Migrate()
cors = CORS()

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=Config.CELERY_BROKER_URL,
        backend=Config.CELERY_RESULT_BACKEND,
        include=['CRON.celery_tasks']
    )
    celery.conf.update(
        task_serializer=Config.CELERY_TASK_SERIALIZER,
        accept_content=Config.CELERY_ACCEPT_CONTENT,
        result_serializer=Config.CELERY_RESULT_SERIALIZER,
        timezone=Config.CELERY_TIMEZONE,
        enable_utc=Config.CELERY_ENABLE_UTC,
        beat_schedule_filename=Config.CELERY_BEAT_SCHEDULE_FILENAME,
        beat_schedule=Config.CELERY_BEAT_SCHEDULE
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, supports_credentials=True)

    celery = make_celery(app)
    app.extensions['celery'] = celery

    from API.clients.routes import clients_blueprint
    from API.appointments.routes import appointment_blueprint
    from API.businesses.routes import business_blueprint
    from API.reviews.routes import reviews_blueprint
    from API.ratings.routes import ratings_blueprint
    from API.notifications.routes import notifications_blueprint
    from API.sales.routes import sales_blueprint
    from API.expense_accounts.routes import accounts_blueprint
    from API.expenses.routes import expenses_blueprint
    from API.inventory.routes import inventory_blueprint
    from API.staff.routes import staff_blueprint
    from API.services.routes import services_blueprint
    from API.admin.routes import admin_blueprint
    from API.messaging.routes import messaging_blueprint
    from API.gallery.routes import gallery_blueprint

    app.register_blueprint(clients_blueprint)
    app.register_blueprint(appointment_blueprint)
    app.register_blueprint(business_blueprint)
    app.register_blueprint(reviews_blueprint)
    app.register_blueprint(ratings_blueprint)
    app.register_blueprint(notifications_blueprint)
    app.register_blueprint(sales_blueprint)
    app.register_blueprint(accounts_blueprint)
    app.register_blueprint(expenses_blueprint)
    app.register_blueprint(inventory_blueprint)
    app.register_blueprint(staff_blueprint)
    app.register_blueprint(services_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(messaging_blueprint)
    app.register_blueprint(gallery_blueprint)

    return app

celery = make_celery(create_app())