from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.ext import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), unique=False, nullable=False)
    position = db.Column(db.String(120), unique=False, nullable=False)
    role = db.Column(db.String(15), unique=False, nullable=False)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    reports = db.relationship('Report', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'User {self.username}'

    def __init__(self, username: str, password: str, position: str, role: str = 'manager') -> None:
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.position = position
        self.role = role

    def verify_password(self, pwd: str) -> bool:
        return check_password_hash(self.password_hash, pwd)

    def is_admin(self) -> bool:
        return self.role == 'admin'

    def add_task(self, task_title: str, task_desc: str):
        task = Task(task_title=task_title,
                    task_desc=task_desc, author_id=self.id)
        db.session.add(task)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_title = db.Column(db.String(15), unique=False, nullable=False)
    task_desc = db.Column(db.String(1200), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))

    def __repr__(self):
        return f'task {self.task_title}'

    @staticmethod
    def for_today():
        return (func.date(Task.created_at) == func.curdate())

    @staticmethod
    def for_today_without_report():
        return (func.date(Task.created_at) == func.curdate(), Task.report_id == None)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_title = db.Column(db.String(15), unique=False, nullable=False)
    report_desc = db.Column(db.String(1200), unique=False, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task = db.relationship('Task', backref='report')

    def __repr__(self):
        return f'report {self.report_title}'

    @staticmethod
    def for_today():
        return (func.date(Report.created_at) == func.curdate())