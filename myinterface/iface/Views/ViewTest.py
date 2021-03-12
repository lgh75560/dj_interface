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

    def update_one_test(self, request):
        """全部信息更新"""
        if request.method == 'POST':
            data = json.loads(request.body)
            test_id = data.get('id', None)
            suit_id = data.get('suit_id', None)
            test_name = data.get('case_name', None)
            test_url = data.get('case_url', None)
            test_method = data.get('case_method', None)
            test_header = data.get('case_header_id', None)
            test_json = data.get('case_json', None)
            test_data = data.get('case_data', None)
            test_source_address = data.get('source_address', None)
            test_expected = data.get('case_expected', None)
            test_match_type = data.get('result_match_type', None)
            test_replace = data.get('replace_name', None)

        else:
            return JsonResponse({"msg": "不支持非post"})

        target_test = ITest.objects.filter(id=test_id)
        if len(target_test) > 0:

            target_test[0].case_header_id = test_header
            target_test[0].suit_id = suit_id
            target_test[0].case_name = test_name
            target_test[0].case_header_id = test_header
            target_test[0].case_url = test_url
            target_test[0].case_method = test_method
            target_test[0].case_json = test_json
            target_test[0].case_data = test_data
            target_test[0].source_address = test_source_address
            target_test[0].case_expected = test_expected
            target_test[0].replace_name = test_replace
            target_test[0].result_match_type = test_match_type

            try:
                target_test[0].save()
            except Exception as e:
                return JsonResponse({"msg": "异常%s" % e})
            return JsonResponse({"msg": "保存成功", "retcode": 0})
        else:
            return JsonResponse({"msg": "有数据为空，请检查", "retcode": -1})

    def get_test_by_id(self, request):
        """通过id获取用例"""
        if not request.body:
            return JsonResponse({"msg": "请输入id"})
        data = json.loads(request.body)
        if "test_id" in data:
            test_id = data.get('test_id', None)
            print("查询的用例id %s" % test_id)
        else:
            return JsonResponse({"msg": "请输入id为空，查询失败"})
        if str(test_id) == "":
            return JsonResponse({"msg": "请输入id", "retcode": -1})

        i_test = ITest.objects.filter(id=test_id)
        if len(i_test) > 0:
            return JsonResponse({"data": i_test[0].to_dict(), "retcode": 0})
        else:
            return JsonResponse({"msg": "查询结果为空，查询失败", "retcode": -1})

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


