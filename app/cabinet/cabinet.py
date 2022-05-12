from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from app.auth.auth import role_required
from app.forms import TaskForm, ReportForm
from app.ext import db
from app.models import Task

cabinet_bp = Blueprint('cabinet_bp', __name__, template_folder='templates')


@cabinet_bp.route('/', methods=['GET'])
@login_required
@role_required('manager')
def manager_panel():
    form_task = TaskForm()
    form_report = ReportForm()
    user_tasks = current_user.tasks.filter(Task.for_today())
    return render_template('manager.html', user_tasks=user_tasks, form_task=form_task, form_report=form_report)


@cabinet_bp.route('/add_task', methods=['POST'])
@login_required
@role_required('manager')
def add_task():
    form_task = TaskForm()
    if form_task.validate_on_submit():
        current_user.add_task(
            task_title=form_task.task_title.data, task_desc=form_task.task_desc.data)
        db.session.commit()
        flash('Задача успешно добавлена!', 'success')
        return redirect(url_for('cabinet_bp.manager_panel'))


@cabinet_bp.route('/add_report', methods=['POST'])
@login_required
@role_required('manager')
def add_report():
    form_report = ReportForm()
    if form_report.validate_on_submit():
        report_title = form_report.report_title.data
        # report_desc = add_report_form.report_desc.data
        # current_user.add_task(task_title=task_title, task_desc=task_desc)
        # db.session.commit()
        flash(f'Отчет "{report_title}" успешно добавлен!', 'success')
        return redirect(url_for('cabinet_bp.manager_panel'))


@cabinet_bp.route('/admin', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_panel():
    return render_template('admin.html')
