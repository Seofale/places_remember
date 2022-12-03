from flask import Flask

from app.core.routers import bp
from app.core.models import db, lm
from app.core.config import SECRET_KEY


def create_application():
    application = Flask(__name__)
    application.secret_key = SECRET_KEY
    application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
    application.register_blueprint(bp)
    db.init_app(application)
    lm.init_app(application)

    with application.app_context():
        db.create_all()

    return application


app = create_application()
