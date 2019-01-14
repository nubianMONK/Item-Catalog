from flask import Blueprint

bp = Blueprint('catalogapp', __name__, template_folder='templates')

# This is to avoid circular imports in flask
from catalog.catalogapp import app_views
