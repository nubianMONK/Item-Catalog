import os
from catalog import create_app
from catalog.catalogapi.models import db
from catalog.catalogapi.models import User, Item, Category
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

app = create_app(os.getenv('FLASK_ENV') or 'config.DevelopmentConfig')
manager = Manager(app)
server = Server(host='0.0.0.0', port=8000)


def make_shell_context():
    return dict(app=app, db=db, User=User, Item=Item, Category=Category)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', server)



if __name__ == '__main__':
    manager.run()
