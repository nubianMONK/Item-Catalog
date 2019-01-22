from flask import Blueprint

bp = Blueprint('catalogapp', __name__, template_folder='templates')

# Module is imported below.This is to avoid circular dependencies in flask
from catalog.catalogapp import app_views # noqa
