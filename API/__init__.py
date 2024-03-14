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


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, supports_credentials=True)

    from API.clients.routes import clients_blueprint

    app.register_blueprint(clients_blueprint)

    return app
