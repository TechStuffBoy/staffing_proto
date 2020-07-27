import os
basedir = os.path.abspath(os.path.dirname(__file__))

# To load for production
from dotenv import load_dotenv
load_dotenv('.env')
load_dotenv('.flaskenv')

config_name = os.environ.get('FLASK_CONFIG')

# config.py


class Config(object):
    """
    Common configurations
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # For Image Upload
    IMAGE_UPLOADS = os.path.join(basedir, 'instance', 'image_uploads')
    ALLOWED_IMAGE_EXTENSIONS = ["JPEG", "JPG", "PNG", "GIF"]
    MAX_IMAGE_FILESIZE = 0.5 * 1024 * 1024

    # For File upload
    FILE_UPLOADS = os.path.join(basedir, 'instance', 'file_uploads')
    ALLOWED_FILE_EXTENSIONS = ["PDF", "DOCX", "DOC"]
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    # Email Server Details
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = '"NTech Global" <noreply@ntekglobal.com>'
    ADMINS = ['<your-username>@email.com']

# Put any configurations here that are common across all environments


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = True
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    

class ProductionConfig(Config):
    """
    Production configurations
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
