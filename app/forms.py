from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired(message='Введите имя'), Length(
        min=4, max=30, message='Имя должно быть от 4 до 30 символов')], render_kw={"placeholder": "Введите имя пользователя"})
    password = StringField('Пароль', validators=[DataRequired()], render_kw={
                           "placeholder": "Введите пароль"})
    submit = SubmitField('ВОЙТИ')


class TaskForm(FlaskForm):
    task_title = StringField('Название задачи', validators=[DataRequired(message='Введите название'), Length(
        min=4, max=15, message='Имя должно быть от 4 до 15 символов')], render_kw={"placeholder": "Ввелите название для задачи"})
    task_desc = CKEditorField('Описание задачи')


class ReportForm(FlaskForm):
    report_title = StringField('Название отчета', validators=[DataRequired(message='Введите название'), Length(
        min=4, max=15, message='Имя должно быть от 4 до 15 символов')], render_kw={"placeholder": "Ввелите название для отчета"})
    report_desc = CKEditorField('Отчет')
