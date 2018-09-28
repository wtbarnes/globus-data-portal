"""
Blueprint for tasks
"""
from flask import Blueprint, render_template

from . import scheduler
from .util.transfer import Transfer

bp = Blueprint('tasks', __name__, url_prefix='/tasks')


@bp.route('/list')
def tasks():
    tasks = []
    t = Transfer()
    for j in scheduler.get_jobs():
        tasks.append({
            'source': t.get_endpoint_name_from_id(j.args[0]),
            'target': t.get_endpoint_name_from_id(j.args[1]),
            'date': j.next_run_time.strftime('%H:%M:%S %m/%d/%Y')})
    return render_template('tasks.html', tasks=tasks)
