from flask import Flask
from flask_login import LoginManager
from config import Config
from app.database import db, migrate
from app.utils import initialize_defaults

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.models.user import User
    from app.models.group import Group
    from app.models.ticket import Ticket
    from app.models.status import Status
    from app.models.role import Role

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, user_id)

    with app.app_context():
        db.create_all()

    from app.views.auth_views import auth_blueprint
    from app.views.user_views import user_blueprint
    from app.views.group_views import group_blueprint
    from app.views.ticket_views import ticket_blueprint
    from app.views.home_views import home_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(group_blueprint)
    app.register_blueprint(ticket_blueprint)
    app.register_blueprint(home_blueprint)

    return app
