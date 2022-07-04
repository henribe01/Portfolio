from flask import Blueprint

bp = Blueprint('admin', __name__)

from portfolio.admin import routes