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

    def update_test(self, request):
        if not request.body:
            return JsonResponse({"msg": "无操作"})
        data = json.loads(request.body)
        if "id" in data:
            test_id = data.get('id', None)
            test_is_able = data.get('is_able', False)
            print(test_id)
            test_is_able
            up_test = ITest.objects.filter(id=test_id)
            if len(up_test) > 0:
                # print(up_test[0].to_dict())
                up_test[0].is_able = (test_is_able is True)
                # print(up_test[0].to_dict())
                up_test[0].save()
                return JsonResponse({"msg": "更新成功", "retcode": 0})
            else:
                return JsonResponse({"msg": "更新失败，查询结果为空", "retcode": -1})

        else:
            return JsonResponse({"msg": "查询用例id为空，更新失败", "retcode": -1})

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
        is_str = False
        try:
            t = int(test_info)
        except Exception as ee:
            is_str = True

        if not is_str:
            # 如果是int 类型，则是查询指定test
            test_res = ITest.objects.filter(id=test_info)
            print("是 int")

        if is_str:
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


