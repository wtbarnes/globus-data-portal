"""
Scheduler to create Globus transfers
"""
import secrets

# from apscheduler.schedulers.background import BackgroundScheduler as Scheduler
from flask_apscheduler import APScheduler as Scheduler

from .transfer import Transfer


class TransferScheduler(Scheduler):

    @staticmethod
    def task(source_id, target_id, items):
        return Transfer().transfer_data(source_id, target_id, items)

    def add_date_job(self, date, source_id, target_id, items,):
        task_id = secrets.token_hex()
        return self.add_job(task_id, self.task, trigger='date', run_date=date,
                            args=[source_id, target_id, items])

    def add_cron_job(self, cron_args, source_id, target_id, items,):
        task_id = secrets.token_hex()
        return self.add_job(task_id, self.task, trigger='cron', args=[source_id, target_id, items],
                            **cron_args)
