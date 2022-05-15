from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from wtforms import BooleanField
from app.auth.auth import role_required
from app.forms import TaskForm, ReportForm
from app.ext import db
from app.models import Task, Report, User

cabinet_bp = Blueprint('cabinet_bp', __name__, template_folder='templates')


@cabinet_bp.route('/', methods=['GET'])
@login_required
@role_required('manager')
def manager_panel():
    form_task = TaskForm()
    user_tasks = current_user.tasks.filter(Task.for_today()).all()
    user_reports = current_user.reports.filter(Report.for_today()).all()
    task_to_report = []
    for task in user_tasks:
        if not task.report_id:
            task_id = f'task_{task.id}'
            task_to_report.append(task_id)
            setattr(ReportForm, task_id, BooleanField(task.task_title))
    form_report = ReportForm()

    context = {
        'user_tasks': user_tasks,
        'task_to_report': task_to_report,
        'form_task': form_task,
        'form_report': form_report,
        'user_reports': user_reports
    }

    return render_template('manager.html', **context)


@cabinet_bp.route('/add_task', methods=['POST'])
@login_required
@role_required('manager')
def add_task():
    form_task = TaskForm()
    if form_task.validate_on_submit():
        new_task = Task(task_title=form_task.task_title.data,
                        task_desc=form_task.task_desc.data)
        db.session.add(new_task)
        current_user.tasks.append(new_task)
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
        report_desc = form_report.report_desc.data
        new_report = Report(report_title=report_title, report_desc=report_desc)
        current_user.reports.append(new_report)
        for task in current_user.tasks.filter(*Task.for_today_without_report()).all():
            if form_report[f'task_{task.id}'].data:
                new_report.task.append(task)
        db.session.commit()
        flash(f'Отчет {report_title} успешно добавлен!', 'success')
        return redirect(url_for('cabinet_bp.manager_panel'))


@cabinet_bp.route('/admin/', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def admin_panel():
    all_users_list = User.query.filter_by(role='manager').all()
    return render_template('admin/managers.html', all_users_list=all_users_list)


@cabinet_bp.route('/admin/<user_id>/')
@login_required
@role_required('admin')
def manager_stats(user_id):

    data = User.query.options(db.joinedload(User.tasks)).options(db.joinedload(User.reports)).get(user_id)
    user = {'username': data.username, 'position':  data.position}
    tasks_no_reports = []
    reports = {}
    for t in data.tasks:
        if t.report:
            if reports.get(t.report):
                reports[t.report.id]['tasks'].append(t)
            else:
                reports[t.report.id] = {'report': t.report, 'tasks': [t]}
        else:
            tasks_no_reports.append(t)

    return render_template('admin/manager-reports.html', user=user, reports=reports)
