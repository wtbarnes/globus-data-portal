"""
Blueprint for tasks
"""
import sys
import datetime

from flask import Blueprint, render_template, request, redirect

from . import scheduler
from .util.transfer import Transfer
from .forms.add_task import AddTaskForm, CronTaskForm

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
    t = Transfer()
    endpoints = [(e['id'], e['display_name']) for e in t.endpoints]
    form.source.choices = endpoints
    form.target.choices = endpoints
    task_added = False
    if form.validate_on_submit():
        if form.use_cron.data is True:
            scheduler.add_cron_job(
                {field.id: field.data for field in form
                 if field.id in ('year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second')
                 and field.data != -1},
                form.source.data,
                form.target.data,
                [{'source': form.source_file.data,
                  'target': form.target_file.data}, ],)
        else:
            scheduler.add_date_job(
                form.date.data,
                form.source.data,
                form.target.data,
                [{'source': form.source_file.data,
                  'target': form.target_file.data}, ],)
        task_added = True
    return render_template('add_task.html', form=form, task_added=task_added)


@bp.route('/remove-<task_id>')
def remove_task(task_id):
    scheduler.remove_job(task_id)
    return redirect('/tasks/list')
