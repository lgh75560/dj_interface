# -*- coding: utf-8 -*-
# @Time    : 2021/2/8 11:52
# @Author  : gh
# @Software: PyCharm

from ..models import TestResult
from ..models import ITest
from ..models import TestRun
from ..models import HeaderManager
from ..models import TestSuit
from django.http import HttpResponse
from django.http import JsonResponse
from ..common_ import *
from ..http_ import HttpEntiry
import json
from django.db.models import Avg, Max, Min
from ..bot_qywx import QywxBot
from ..qq_mail import SendMail
import socket


class RunResult:
    server_host = ""

    def run_run(self, request):
        """通过运行id，执行结果集"""
        if not request.body:
            return JsonResponse({"msg": "请勾选用例", "recode": -1})
        data = json.loads(request.body)
        if "run_id" in data:
            run_id = data.get('run_id', None)
        else:
            return JsonResponse({"msg": "运行集，选择为空，执行结果失败"})

        return self.run_run_by_id(run_id)

    def run_run_by_id(self, run_id):
        """跟进runid 运行运行集合，可以外部调用"""
        # 先通过run组装运行结果testResult
        test_run = TestRun.objects.filter(id=run_id)
        old_result = TestResult.objects.filter(run_id=run_id)
        is_has_old = True
        run_counter = 0
        if not old_result:
            # 是否有同运行集，历史记录
            is_has_old = False
            run_counter = 0
        if is_has_old:
            # 逆序，取第一个作为历史counter，新的counter + 1
            tr_his = TestResult.objects.filter(run_id=run_id).values('run_counter').order_by("-run_counter")
            run_counter = tr_his[0]['run_counter'] + 1

        if test_run:
            test_ids = test_run[0].run_ids
            for test_id in str(test_ids).split("#"):
                print(run_counter)
                if test_id == "":
                    continue
                itest_id = int(test_id)

                tr = TestResult(run_id=run_id, itest_id=itest_id, run_counter=run_counter)
                tr.save()

        choose_resultrun = TestResult.objects.filter(run_id=run_id, run_counter=run_counter)
        if len(choose_resultrun) > 0:
            for test_run in choose_resultrun:
                HttpEntiry(test_run).run_test()
            return JsonResponse({"msg": "运行完毕", "retcode": 0})
        else:
            return JsonResponse({"msg": "没有找到运行集，执行结果失败", "retcode": -1})

    def get_run_select(self, request):
        """返回前端封装级联菜单"""
        all_result = TestResult.objects.values("run_id", "run_counter").distinct()
        run_dict = {}
        for res in all_result:
            cur_run_id = res["run_id"]
            cur_counter = res['run_counter']
            if int(cur_run_id) in run_dict:
                if int(cur_counter) in run_dict[cur_run_id]:
                    pass
                else:
                    # 不在的话，就追加一下
                    run_dict[cur_run_id].append(cur_counter)
            else:
                # 初始化
                run_dict[cur_run_id] = [cur_counter]

        data = []
        for k, v in run_dict.items():
            # k run_id   v 下面的次数
            print(k, v)
            # counter 逆序，让最大的在前面
            v.reverse()
            run_name = k
            irun = TestRun.objects.filter(id=k)
            if len(irun) > 0:
                run_name = irun[0].run_name

            child_lst = []
            for child in v:
                child_lst.append({"label": str(run_name) + "#" + str(child), "value": child})
            data.append({"label": str(run_name), "value": k, "children": child_lst})

        return JsonResponse({"data": data, "retcode": 0})

    def get_report(self, request):
        """根据，run_id counter 生成报告"""
        run_id = None
        run_counter = None

        if request.method == 'POST':
            if not request.body:
                return JsonResponse({"msg": "没有参数"})
            data = json.loads(request.body)
            if "run_id" in data:
                run_id = data.get('run_id', None)
                run_counter = data.get('run_counter', None)

        if run_id is not None and str(run_id).strip() != "":
            test_res = TestResult.objects.filter(run_id=int(run_id), run_counter=run_counter)

            t_run = TestRun.objects.filter(id=run_id)
            run_name = ""
            if len(t_run) > 0:
                run_name = t_run[0].run_name

            pass_count = 0
            fail_count = 0
            unkown_count = 0
            for res in test_res:
                if res.result_pass is True:
                    pass_count += 1
                    continue
                if res.result_pass is False:
                    fail_count += 1
                    continue
                unkown_count += 1

            lst2 = []
            for t in test_res:
                try:
                    dict_result = t.to_dict()

                    try:
                        get_test = ITest.objects.get(id=dict_result["itest_id"])
                    except Exception as e3:
                        continue
                    dict_test = get_test.to_dict()

                    try:
                        get_suit = TestSuit.objects.get(id=dict_test["suit_id"])
                    except Exception as e3:
                        continue
                    dict_suit = get_suit.to_dict()

                    z = dict(dict_suit, **dict_test)
                    y = dict(z, **dict_result)

                    result_match_type = y["result_match_type"]
                    y["result_match_type"] = "相等" if result_match_type == MatchMethod.EQAUL.value else "包含"

                    test_method = y['case_method']
                    y['case_method'] = "GET" if test_method == HttpMethod.GET.value else "POST"

                    lst2.append(y)
                except Exception as e1:
                    pass
            return JsonResponse({"data": lst2, "retcode": 0, "pass_count": pass_count, "fail_count": fail_count, "unkown_count": unkown_count, "run_name": run_name})
        else:
            return JsonResponse({"msg": "rund_id为空，无法获取数据", "retcode": -1})

    def get_report_by_run_id(self, run_id):
        """通过run id 获取最新一次运行结果"""
        run_max_count = TestResult.objects.filter(run_id=run_id).order_by('run_counter').aggregate(Max('run_counter'))
        print("最大运行次数 %s" % run_max_count)
        test_res = TestResult.objects.filter(run_id=run_id, run_counter=run_max_count['run_counter__max'])
        t_run = TestRun.objects.filter(id=run_id)
        run_name = ""
        if len(t_run) > 0:
            run_name = t_run[0].run_name

        pass_count = 0
        fail_count = 0
        unkown_count = 0
        fail_lst = []
        for res in test_res:
            if res.result_pass is True:
                pass_count += 1
                continue
            if res.result_pass is False:
                fail_count += 1
                continue
            unkown_count += 1

        lst2 = []
        for t in test_res:
            try:
                dict_result = t.to_dict()

                try:
                    get_test = ITest.objects.get(id=dict_result["itest_id"])
                except Exception as e3:
                    continue
                dict_test = get_test.to_dict()

                try:
                    get_suit = TestSuit.objects.get(id=dict_test["suit_id"])
                except Exception as e3:
                    continue
                dict_suit = get_suit.to_dict()

                if t.result_pass is False:
                    fail_lst.append("用例名称 %s，响应时间 %s" % (dict_test["case_name"], t["request_time"]))

                z = dict(dict_suit, **dict_test)
                y = dict(z, **dict_result)

                result_match_type = y["result_match_type"]
                y["result_match_type"] = "相等" if result_match_type == MatchMethod.EQAUL.value else "包含"

                test_method = y['case_method']
                y['case_method'] = "GET" if test_method == HttpMethod.GET.value else "POST"

                lst2.append(y)
            except Exception as e1:
                pass

        try:
            myname = socket.getfqdn(socket.gethostname())
            # 获取本机ip
            myaddr = socket.gethostbyname(myname)
        except:
            myaddr = 'localhost'
        report_url = "http://" + myaddr + ":8001/test_report?run_id=" + str(run_id) + "&counter_id=" + str(run_max_count['run_counter__max'])
        print(report_url)
        if fail_count > 0:
            QywxBot().send_text_use_test_group(type_text="业务-%s出现错误，from django web" % run_name, pass_count=pass_count, fail_count=fail_count, fail_list=fail_lst, url=report_url)
            SendMail().send_report_with_dict(title="业务-%s出现错误，from django web" % run_name, case_list=lst2, total=len(test_res), pass_count=pass_count, fail_count=fail_count, to_mail="liaoguohu@jiwu.com", attach_url=report_url)