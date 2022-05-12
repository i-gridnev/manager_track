from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


ckeditor = CKEditor()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
