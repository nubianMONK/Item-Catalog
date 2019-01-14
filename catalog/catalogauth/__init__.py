
from flask import Blueprint

bp = Blueprint('catalogauth', __name__)

# This is to avoid circular imports in flask
from catalog.catalogauth import auth_views
