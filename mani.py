from appLL import db, app
from appLL.models import Users
from appLL.externo import DevelopmentConfig, ProductionConfig


if __name__ == "__main__":

    app.config.from_object(ProductionConfig)

    
    with app.app_context():
        db.create_all()
    
    # Ejecuta la aplicación
    app.run(debug=app.config['DEBUG'], port=3200)

#if __name__ == "__main__":
#    with app.app_context():
        
#        db.create_all()
        
        
#    app.run(debug=True, port=3200)