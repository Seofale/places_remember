from flask import Flask

from . routers import bp
from . models import db, lm


def create_application():
    application = Flask(__name__)
    application.secret_key = 'some_secret'
    application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
    application.register_blueprint(bp)
    db.init_app(application)
    lm.init_app(application)

    with application.app_context():
        db.create_all()

    return application


app = create_application()
