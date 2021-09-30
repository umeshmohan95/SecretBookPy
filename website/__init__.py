from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()   #db is the object we use to add remove and any other operation
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "All is well"      #encrypt cookies and session data related to website
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'   #SQL alchemy database location details
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')   # url_prifix guide how to access all the url stored inside blurprint
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # show where to go if not login
    login_manager.init_app(app)             # it will tell login manager which app we are using

    # Telling flask how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  #get always look for unique id...

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('database Created!')