from flask import Blueprint

bp = Blueprint('main', __name__)

from portfolio.main import routes
