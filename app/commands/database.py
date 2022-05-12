import click
from flask.cli import with_appcontext
from app.models import Report, User, Task
from app.ext import db


@click.command('initdb')
@with_appcontext
def initdb_with_dummy():
    dummy_users = [
        User(username='admin', password='1234', position='super puper admin', role='admin'),
        User(username='manager', password='4444',
             position='Ответственный по воде'),
    ]
    db.session.add_all(dummy_users)

    task1 = Task(task_title='Some one', task_desc='Very long description etc.............')
    task2 = Task(task_title='Another one', task_desc='Very very long description etc.............')
    task3 = Task(task_title='Secondary task', task_desc='Very long description etc.............')
    task4 = Task(task_title='Very hard one', task_desc='Very very long description etc.............')
    task5 = Task(task_title='Only for admin', task_desc='Very very long description etc.............')
    task6 = Task(task_title='adminsmt', task_desc='Very very long description etc.............')

    db.session.add_all([task1, task2, task3, task4, task5, task6])

    report = Report(report_title='My new report', report_desc='With some data to consult')
    dummy_users[1].reports.append(report)
    
    
    report.task.extend([task1, task2, task3, task4])
    dummy_users[1].tasks.extend([task1, task2, task3, task4])


    dummy_users[0].tasks.extend([task5, task6])




    db.session.commit()


@click.command('flushdb')
@with_appcontext
def flusdb():
    db.session.query(Task).delete()
    db.session.query(User).delete()
    db.session.commit()

@click.command('dropdb')
@with_appcontext
def dropdb():
    db.drop_all()
    db.create_all()
