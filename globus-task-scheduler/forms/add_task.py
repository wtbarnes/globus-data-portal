"""
Form for adding a task to the scheduler
"""
import datetime
import calendar

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Optional


class AddTaskForm(FlaskForm):
    # Endpoints and files
    source = SelectField('source', validators=[DataRequired()], description='Source')
    target = SelectField('target', validators=[DataRequired()], description='Target')
    source_file = StringField('source_file', validators=[DataRequired()],
                              description='Source File')
    target_file = StringField('target_file', validators=[DataRequired()],
                              description='Target File')
    # Date
    date = DateTimeField('date', format='%m/%d/%Y %H:%M:%S',
                         description='Date', validators=[Optional()])
    # Cron
    use_cron = BooleanField('use_cron', default=False, description='Use Cron',
                            validators=[DataRequired()])
    cur_year = datetime.datetime.now().year
    year = SelectField(
        'year',
        choices=[(-1, '')] + [(i, i) for i in range(cur_year, cur_year+100)],
        description='Year',
        coerce=int,
        default=-1)
    month = SelectField(
        'month',
        choices=[(-1, '')] + [(i, calendar.month_name[i]) for i in range(1, 13)],
        description='Month',
        coerce=int,
        default=-1)
    day = SelectField(
        'day',
        choices=[(-1, '')] + [(i, i) for i in range(1, 32)],
        description='Day',
        coerce=int,
        default=-1)
    week = SelectField(
        'week',
        choices=[(-1, '')] + [(i, i) for i in range(1, 54)],
        description='Week',
        coerce=int,
        default=-1)
    day_of_week = SelectField(
        'day_of_week',
        choices=[(-1, '')] + [(i, calendar.day_name[i]) for i in range(7)],
        description='Week Day',
        coerce=int,
        default=-1)
    hour = SelectField(
        'hour',
        choices=[(-1, '')] + [(i, i) for i in range(24)],
        description='Hour',
        coerce=int,
        default=-1)
    minute = SelectField(
        'minute',
        choices=[(-1, '')] + [(i, i) for i in range(60)],
        description='Minute',
        coerce=int,
        default=-1)
    second = SelectField(
        'second',
        choices=[(-1, '')] + [(i, i) for i in range(60)],
        description='Second',
        coerce=int,
        default=-1)
    # Send
    submit = SubmitField(description='Add Transfer')


class CronTaskForm(FlaskForm):
    ...
