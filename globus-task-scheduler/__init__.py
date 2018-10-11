"""
App factory
"""
import os
import datetime

from flask import Flask
from .util.scheduler import TransferScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

# Create scheduler
scheduler = TransferScheduler()


class Config(object):
    SECRET_KEY = 'dev'
    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    SCHEDULER_API_ENABLED = True
    # DATABASE=os.path.join(app.instance_path, 'globus-task-scheduler.sqlite')


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config())
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # Register blueprints
    from . import home, transfers, tasks
    app.register_blueprint(home.bp)
    app.register_blueprint(transfers.bp)
    app.register_blueprint(tasks.bp)
    # Register scheduler
    scheduler.init_app(app)
    scheduler.start()

    return app
