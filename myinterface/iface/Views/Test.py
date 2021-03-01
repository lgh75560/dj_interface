# -*- coding: utf-8 -*-
# @Time    : 2021/3/1 11:35
# @Author  : gh
# @Software: PyCharm

from ..models import TestResult
from ..models import ITest
from ..models import TestSuit
from ..models import HeaderManager
from django.http import HttpResponse
from django.http import JsonResponse
from ..common_ import *
import json
from django.db.models import Q


class TestManager:
    """管理测试用例，增删改查"""

    def get_test_from_info(self, request):
        """查询用例"""
        if not request.body:
            return JsonResponse({"msg": "请勾选用例"})
        data = json.loads(request.body)
        if "test_info" in data:
            test_info = data.get('test_info', None)
            print(test_info)
        else:
            return JsonResponse({"msg": "查询信息为空，选择为空，执行结果失败"})

        lst = []
        if str(test_info).strip() == "":
            return JsonResponse({"msg": "查询信息为空，执行结果失败"})

        test_res = []
        is_druged = False
        if isinstance(test_info, int):
            # 如果是int 类型，则是查询指定test
            test_res = ITest.objects.filter(id=test_info)
            print("是 int")
            is_druged = True
        if isinstance(test_info, str) and not is_druged:
            # 则是批量的
            # like "A" Or b like "A"
            test_res = ITest.objects.filter(Q(case_name__contains=test_info) | Q(case_url__contains=test_info))

            print("是 str")

        if len(test_res) > 0:
            for i_test in test_res:
                dict_result = i_test.to_dict()

                result_match_type = dict_result["result_match_type"]
                dict_result["result_match_type"] = "相等" if result_match_type == MatchMethod.EQAUL.value else "包含"

                test_method = dict_result['case_method']
                dict_result['case_method'] = "GET" if test_method == HttpMethod.GET.value else "POST"

                t_h = HeaderManager.objects.filter(id=i_test.case_header_id)

                dict_result['case_header_name'] = t_h[0].header_name

                suit_all = TestSuit.objects.filter(id=i_test.suit_id)

                dict_result['case_suit_name'] = suit_all[0].suit_name

                lst.append(dict_result)

            return JsonResponse({"data": lst})
        else:
            return JsonResponse({"msg": "没有找到运行集，执行结果失败"})


