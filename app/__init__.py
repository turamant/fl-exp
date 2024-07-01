from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager

# инициализация объектов базы данных
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)  # Инициализируем Flask-Login
     
    from app.models import User  # Импорт User здесь для избежания круговой зависимости

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) 

    from app.main import bp as main_bp
    from app.auth import auth as auth_blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_blueprint)

    return app
