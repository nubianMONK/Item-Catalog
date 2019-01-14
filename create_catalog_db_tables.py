from catalog import create_app
from catalog.catalogapi.models import db
import os


app = create_app(os.getenv('FLASK_ENV') or 'config.DevelopmentConfig')


def stand_up():

    with app.app_context():
        db.create_all()
        db.session.commit()
        print("Database tables created")


stand_up()
