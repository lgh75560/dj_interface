# -*- coding: utf-8 -*-
# @Time    : 2021/3/5 11:19
# @Author  : gh
# @Software: PyCharm
import json
from django.http import JsonResponse
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.triggers.interval import IntervalTrigger

from ..Views import ViewRunResult
scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), 'default')
import datetime


class TimerView:
    # 与前端的接口
    def add_timer_job(self, request):
        if request.method == 'POST':
            if not request.body:
                return JsonResponse({"msg": "请勾选用例", "recode": -1})
            data = json.loads(request.body)
            if "run_id" in data:
                run_id = data.get('run_id', None)
                interval_hour = data.get('interval_hour', None)
                run_name = data.get('run_name', None)
            else:
                return JsonResponse({"msg": "run_id为空，添加定时器失败", "retcode": -1})
            if run_id is None or interval_hour is None:
                return JsonResponse({"msg": "run_id 或interval_seconds为空，添加定时器失败", "retcode": -1})

            try:
                # 创建任务
                # kwargs 支持字典
                # args 不支持字典
                interval_seconds = float(interval_hour) * 60 * 60
                if interval_seconds < 10:
                    interval_seconds = 10
                job = scheduler.add_job(self.timming_run_result, trigger='interval', kwargs={"run_id": run_id}, seconds=interval_seconds, id=run_name)  # 每隔3h执行一次func

                print(job.name)
                return JsonResponse({"msg": "添加定时器成功 %s" % job.id, "retcode": 0})

            except Exception as e:
                return JsonResponse({"msg": "添加定时器失败 %s" % e, "retcode": -1})

    # 具体要执行的代码
    def timming_run_result(self, run_id):
        print(">>执行定时器")
        vr = ViewRunResult.RunResult()
        print(vr.run_run_by_id(run_id))
        print(vr.get_report_by_run_id(run_id))

    def get_all_job(self):
        time_jobs = []
        for j in scheduler.get_jobs():
            job_current = {}
            job_current['id'] = j.id
            job_current['kwargs'] = j.kwargs
            job_current['next_run_time'] = j.next_run_time
            # 是否只运行一次
            job_current['run_once'] = j.coalesce
            job_current['name'] = j.name
            print("interval " + str(j.trigger.interval))
            job_current['interval'] = str(j.trigger.interval)
            print(job_current['interval'])
            time_jobs.append(job_current)
        return JsonResponse({"data": time_jobs, "retcode": 0})

    def remove_job(self, request):
        """接受request版"""
        if request.method == 'POST':
            if not request.body:
                return JsonResponse({"msg": "没有job id", "recode": -1})
            data = json.loads(request.body)
            if "job_id" in data:
                job_id = data.get('job_id', None)

            else:
                return JsonResponse({"msg": "job_id，删除定时器失败", "retcode": -1})

            if job_id is None:
                return JsonResponse({"msg": "job_id为空，删除定时器失败", "retcode": -1})

        return self.remove_job_by_id(job_id)

    def remove_job_by_id(self, job_id):
        """移除定时任务"""
        try:
            target_job = scheduler.get_job(job_id=job_id)
            target_job.remove()
            return JsonResponse({"msg": "移除job %s 成功" % job_id, "retcode": 0})
        except Exception as ee:
            return JsonResponse({"msg": "移除job %s 异常 %s" % (job_id, ee), "retcode": -1})

scheduler.start()

