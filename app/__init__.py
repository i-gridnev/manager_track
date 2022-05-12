from flask import Flask
from app.ext import db, login_manager, ckeditor, migrate
from app.commands.database import initdb_with_dummy, dropdb, flusdb

from app.auth.auth import auth_bp
from app.cabinet.cabinet import cabinet_bp


def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    with app.app_context():
        db.init_app(app)
        migrate.init_app(app, db)
        login_manager.init_app(app)
        ckeditor.init_app(app)

        app.register_blueprint(auth_bp)
        app.register_blueprint(cabinet_bp, url_prefix='/cabinet')

        app.cli.add_command(initdb_with_dummy)
        app.cli.add_command(dropdb)
        app.cli.add_command(flusdb)

        return app
