
from flask import Blueprint

bp = Blueprint('catalogauth', __name__)

# Module is imported below.This is to avoid circular dependencies in flask
from catalog.catalogauth import auth_views # noqa
