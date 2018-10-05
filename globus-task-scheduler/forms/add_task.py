"""
Form for adding a task to the scheduler
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired


class AddTaskForm(FlaskForm):
    source = SelectField('Source', validators=[DataRequired()])
    target = SelectField('Target', validators=[DataRequired()])
    source_file = StringField('Source File', validators=[DataRequired()])
    target_file = StringField('Target File', validators=[DataRequired()])
    date = DateTimeField('Date', validators=[DataRequired()], format='%m/%d/%Y %H:%M:%S')
    submit = SubmitField(description='Add Transfer')
