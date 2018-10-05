"""
Blueprint for tasks
"""
import sys
import datetime

from flask import Blueprint, render_template, request, redirect

from . import scheduler
from .util.transfer import Transfer
from .forms.add_task import AddTaskForm

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('/list')
def list_tasks():
    tasks = []
    t = Transfer()
    for j in scheduler.get_jobs():
        tasks.append({
            'id': j.id,
            'source': t.get_endpoint_name_from_id(j.args[0]),
            'target': t.get_endpoint_name_from_id(j.args[1]),
            'date': j.next_run_time.strftime('%H:%M:%S %m/%d/%Y')})
    return render_template('list_tasks.html', tasks=tasks)


@bp.route('/add', methods=['GET', 'POST'])
def add_task():
    form = AddTaskForm(request.form)
    if form.validate_on_submit():
        scheduler.add_date_job(
            datetime.datetime.strptime(form.date.data, '%m/%d/%Y %H:%M:%S'),
            form.source.data,
            form.target.data,
            [{'source': form.source_file.data,
                'target': form.target_file.data}, ],)
    return render_template('add_task.html', form=form)


@bp.route('/remove-<task_id>')
def remove_task(task_id):
    scheduler.remove_job(task_id)
    return redirect('/tasks/list')
