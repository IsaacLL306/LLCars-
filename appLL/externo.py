#Creo que esto sera para la config
import os
from . import app
from flask import send_from_directory


save_image = os.path.abspath("./appLL/static/uploads")
app.config["UPLOAD_FOLDER"] = save_image

if not os.path.exists(save_image):
    os.makedirs(save_image)

save_news = os.path.abspath("./appLL/static/uploads/news")
app.config["NEWS_IMAGE_FOLDER"] = save_news

if not os.path.exists(save_news):
    os.makedirs(save_news)

@app.route("/uploads/<filename>")
def get_file(filename):    
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


class Config:
    """Configuración base."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'LL_Proyecto306'  # Cambia esto por una clave secreta segura
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # Cambia esto por tu URL de base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Tamaño máximo permitido para subidas: 16 MB
    LOGGING_LEVEL = 'WARNING'  # Nivel de registro por defecto

class DevelopmentConfig(Config):
    """Configuración para desarrollo."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'  # Base de datos específica para desarrollo
    LOGGING_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@host/prod_db'  # Configuración para base de datos en producción
    LOGGING_LEVEL = 'ERROR'

class TestingConfig(Config):
    """Configuración para pruebas."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # Base de datos específica para pruebas
    LOGGING_LEVEL = 'INFO'
