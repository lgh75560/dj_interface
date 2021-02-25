# -*- coding: utf-8 -*-
# @Time    : 2021/2/8 11:52
# @Author  : gh
# @Software: PyCharm

from ..models import TestResult
from ..models import ITest
from ..models import TestSuit
from ..models import HeaderManager
from django.http import HttpResponse
from django.http import JsonResponse
from ..common_ import *
from django.views.decorators.http import require_GET, require_http_methods, require_POST
import json


class TestTesultView:

    def get_test_result(self, request):
        """查询用例"""
        if not request.body:
            return JsonResponse({"msg": "请勾选用例"})
        data = json.loads(request.body)
        if "run_id" in data:
            run_id = data.get('run_id', None)
        else:
            return JsonResponse({"msg": "运行集，选择为空，执行结果失败"})

        lst = []
        choose_resultrun = TestResult.objects.filter(run_id=run_id)
        if len(choose_resultrun) > 0:
            for test_run in choose_resultrun:
                dict_result = test_run.to_dict()

                get_test = ITest.objects.get(id=dict_result["itest_id"])
                dict_test = get_test.to_dict()

                get_suit = TestSuit.objects.get(id=dict_test["suit_id"])
                dict_suit = get_suit.to_dict()

                z = dict(dict_suit, **dict_test)
                y = dict(z, **dict_result)

                result_match_type = y["result_match_type"]
                y["result_match_type"] = "相等" if result_match_type == MatchMethod.EQAUL.value else "包含"

                test_method = y['case_method']
                y['case_method'] = "GET" if test_method == HttpMethod.GET.value else "POST"

                lst.append(y)

            return JsonResponse({"data": lst})
        else:
            return JsonResponse({"msg": "没有找到运行集，执行结果失败"})


