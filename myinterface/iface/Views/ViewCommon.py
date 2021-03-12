# -*- coding: utf-8 -*-
# @Time    : 2021/3/11 12:18
# @Author  : gh
# @Software: PyCharm

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.triggers.interval import IntervalTrigger


scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')


def timmer_start():
    scheduler.start()


def get_timer():
    return scheduler


def timmer_stop():
    scheduler.pause()


# 默认开启
# 这个文件，控制全局静态类
timmer_start()