"""
Form for adding a task to the scheduler
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddTaskForm(FlaskForm):
    source = StringField('Source', validators=[DataRequired()])
    target = StringField('Target', validators=[DataRequired()])
    source_file = StringField('Source File', validators=[DataRequired()])
    target_file = StringField('Target File', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Add Task')
