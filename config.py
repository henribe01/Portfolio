import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(
        os.path.dirname(__file__), 'portfolio.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CAROUSEL_AMOUNT = 3
    PROJECTS_PER_PAGE = 12

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'portfolio/static/img/projects')
    DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'portfolio/static/downloads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    FLATPAGES_EXTENSION = '.md'
    FLATPAGES_ROOT = os.path.join(os.getcwd(), 'portfolio/static/md')
