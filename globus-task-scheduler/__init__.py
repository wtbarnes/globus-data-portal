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
#scheduler.start()

## Dummy jobs
#def hello_world():
#    return 'Hello World!'
#def foo_bar():
#    return 'Foo Bar!'
#scheduler.add_job('hello world', hello_world, trigger='interval', minutes=5)
#scheduler.add_job('foo bar', foo_bar, trigger='date',
#                  run_date=datetime.datetime.now()+datetime.timedelta(days=1))
# future_date = datetime.datetime.now() + datetime.timedelta(days=1)
# scheduler.add_date_job(
#     future_date,
#     '4e3c15d8-6f53-11e8-9327-0a6d4e044368',
#     '944ef3d8-912a-11e8-9674-0a6d4e044368',
#     [{'source': '/storage-home/w/wtb2/data/bundle_heating_model/emission_model.json',
#       'target': '/Users/willbarnes/Desktop/emodel.json'},],
# )


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

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

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
    #scheduler = TransferScheduler()
    scheduler.init_app(app)
    scheduler.start()

    return app
