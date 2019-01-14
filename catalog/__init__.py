from flask import Flask
from flask_migrate import Migrate
from flask_login import current_user
from flask_restful import Api
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer.backend.sqla import SQLAlchemyBackend
from catalog.catalogapi.models import OAuth
# import config


migrate = Migrate()
bootstrap = Bootstrap()
csrfprotect = CSRFProtect()
google_bp = make_google_blueprint()
api = Api()


# application factory pattern - Presentation layer
def create_app(config):

    # create application instance
    app = Flask(__name__)
    app.config.from_object(config)

    from catalog.catalogapi.models import db
    db.init_app(app)

    migrate.init_app(app, db)
    bootstrap.init_app(app)
    csrfprotect.init_app(app)

    from catalog.catalogapi.models import login_manager
    login_manager.init_app(app)
    login_manager.login_view = 'google.login'

    # Register blueprint for the application component
    from catalog.catalogapp import bp as app_bp
    app.register_blueprint(app_bp)

    # Register blueprint for the authentication component
    from catalog.catalogauth import bp as app_auth
    app.register_blueprint(app_auth)

    app.register_blueprint(google_bp, url_prefix="/login")
    google_bp.from_config["session.scope"] = "SCOPE"
    google_bp.backend = SQLAlchemyBackend(OAuth, db.session, user=current_user)

    return app


# Application factory pattern - API Layer
def create_api(config):

    # create application instance
    app = Flask(__name__)
    app.config.from_object(config)

    from catalog.catalogapi.models import db
    db.init_app(app)
    migrate.init_app(app, db)

    from catalog.catalogapi.models import login_manager
    login_manager.init_app(app)
    login_manager.login_view = 'google.login'

    from catalog.catalogapi.endpoints import (
                                            UserAPI, UserListAPI, ItemAPI,
                                            ItemListAPI, CategoryAPI,
                                            CategoryListAPI, ItemsByUserAPI,
                                            ItemsByCategoryAPI, CatalogAPI
                                                )

    # Add API endpoint resources
    api.add_resource(UserAPI, '/api/v1/users/<int:id>', endpoint='user')
    api.add_resource(UserListAPI, '/api/v1/users', endpoint='users')
    api.add_resource(ItemAPI, '/api/v1/items/<int:id>', endpoint='item')
    api.add_resource(ItemListAPI, '/api/v1/items', endpoint='items')
    api.add_resource(CategoryAPI, '/api/v1/categories/<int:id>',
                     endpoint='category')
    api.add_resource(CategoryListAPI, '/api/v1/categories',
                     endpoint='categories')
    api.add_resource(ItemsByUserAPI, '/api/v1/users/<int:id>/items',
                     endpoint='items_by_user')
    api.add_resource(ItemsByCategoryAPI,
                     '/api/v1/categories/<int:id>/items',
                     endpoint='items_by_category')
    api.add_resource(CatalogAPI, '/api/v1/catalog',
                     endpoint='catalog')

    api.init_app(app)

    return app
