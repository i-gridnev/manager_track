from functools import wraps
from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm
from app.models import User
from app.ext import login_manager

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates')


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            if user.is_admin():
                flash(f'Успешный вход {user.username}!', 'success')
                return redirect(url_for('cabinet_bp.admin_panel'))
            return redirect(url_for('cabinet_bp.manager_panel'))
        flash('Пользователь не найден или не верный пароль', 'danger')
    return render_template('login.html', form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

def role_required(role:str):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            if current_user.role == role:
                return func(*args, **kwargs)
            flash('Доступ запрещён!', 'danger')
            return render_template('restricted.html')
        return wrap
    return decorator

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('auth_bp.login'))
