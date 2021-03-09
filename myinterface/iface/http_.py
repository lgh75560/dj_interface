# -*- coding: utf-8 -*-
# @Time    : 2021/2/8 9:03
# @Author  : gh
# @Software: PyCharm

import requests
from .models import TestResult
from .models import ITest
from .models import HeaderManager
import random
from .models import BeforTest
import datetime
from .common_ import *


class HttpEntiry:

    def __init__(self, test_result):
        self.test_result = test_result
        self.replace_data = ""

    def run_test(self, is_save=True, itest=None):
        if not is_save:
            real_test_all = itest
        else:

            try:
                # 整个case 信息
                # 需要配置是，可用状态的，否则不运行
                real_test_all = ITest.objects.get(id=self.test_result.itest_id, is_able=True)
            except Exception as e1:
                return {"msg": "查找不到用例"}
        if real_test_all:
            real_test = real_test_all
            self.init_replace_data(real_test)
            print(self.replace_data)
            if self.replace_data == "":
                return {"msg": "异常，替换字符串为空"}
            header = HeaderManager.objects.filter(id=real_test.case_header_id)
            if len(header) > 0:
                # 拿到的header value
                real_header = header[0].value
                if not str(header).startswith("{"):
                    real_header = "{" + real_header
                if not str(header).endswith("}"):
                    real_header = real_header + "}"
                dict_header = eval(real_header)

                real_url = real_test.case_url
                real_data = real_test.case_data
                real_json = real_test.case_json
                real_post_data = ""
                if str(real_test.replace_name).strip() != "":
                    # 替换字符串为空的，不替换，否则全部替换成手机号了
                    real_url = str(real_test.case_url).replace(real_test.replace_name, self.replace_data)
                    real_data = str(real_test.case_data).replace(real_test.replace_name, self.replace_data)
                    real_json = str(real_test.case_json).replace(real_test.replace_name, self.replace_data)

                if str(real_data).strip() == "" and str(real_json).strip() != "":
                    real_post_data = real_json

                if str(real_data).strip() != "" and str(real_json).strip() == "":
                    real_post_data = real_data
                # 2021年3月2日12:44:29修改，添加json判断
                if str(real_json).strip() != "":
                    dict_header['Content-Type'] = 'application/json'

                real_expected = [real_test.case_expected]
                if "#" in real_test.case_expected:
                    expected_lst = str(real_test.case_expected).split("#")
                    real_expected = expected_lst

                # 是否用包含判断
                real_use_contain = True if real_test.result_match_type == MatchMethod.CONTAIN.value else False

                star_time = datetime.datetime.now()

                print("url %s" % real_url)
                print("header %s" % dict_header)
                print("post_data %s" % real_post_data)
                print("使用包含判断结果：%s" % real_use_contain)
                print("预期结果 %s" % real_expected)

                # print("data encode  %s" % real_post_data.encode('utf-8'))
                http_enty = ""
                # 0 get 1 post
                try:
                    if int(real_test.case_method) == HttpMethod.GET.value:
                        if str(real_data).strip() != "":
                            http_enty = requests.get(url=real_url, params=real_post_data.encode('utf-8'), headers=dict_header)
                        else:
                            http_enty = requests.get(url=real_url, headers=dict_header)

                    if int(real_test.case_method) == HttpMethod.POST.value:
                        http_enty = requests.post(url=real_url, data=real_post_data.encode('utf-8'), headers=dict_header)

                    print(">>未设定内容，没有执行请求")
                except Exception as e:
                    if not is_save:
                        return {"msg": "执行异常，%s" % e, "retcode": -1}

                    self.test_result.result_des = e
                    self.test_result.result_pass = False
                    self.test_result.save()
                    return {"msg": "执行异常，%s" % e}

                end_time = datetime.datetime.now()

                response_text = str(http_enty.text)

                print("请求返回body %s" % response_text)
                is_find_excpectd_str = False
                is_less_than_3s = False
                is_test_pass = True

                # 适配返回体比简单的，简单包含，容易误判
                if real_use_contain:
                    for jj in range(0, len(real_expected)):
                        print(">>查找[包含]对比项 %s" % real_expected[jj])
                        if real_expected[jj] in response_text:
                            is_find_excpectd_str = True
                            print(">>> [包含]结果 %s" % is_find_excpectd_str)
                else:
                    for jj in range(0, len(real_expected)):
                        print(">>查找[相等]对比项 %s" % real_expected[jj])
                        if real_expected[jj] == str(response_text.strip()):
                            is_find_excpectd_str = True
                            print(">>> [相等]结果 %s" % is_find_excpectd_str)

                if http_enty.elapsed.total_seconds() < 3:
                    is_less_than_3s = True

                if http_enty.status_code != 200:
                    is_test_pass = False
                    if not is_save:
                        # 属于异常
                        return {"msg": "status_code %s /n,response body:%s，" % (http_enty.status_code, response_text),
                                "retcode": -1}
                if not is_less_than_3s:
                    is_test_pass = False
                if not is_find_excpectd_str:
                    is_test_pass = False

                self.test_result.start_time = star_time
                self.test_result.end_time = end_time
                if not is_test_pass:
                    self.test_result.result_response = response_text
                if not is_test_pass:
                    self.test_result.header_id = real_test.case_header_id

                self.test_result.response_status = http_enty.status_code
                print("是否通过 %s" % is_test_pass)
                self.test_result.request_url = real_url
                self.test_result.request_json = real_json
                self.test_result.request_data = real_data
                self.test_result.result_pass = is_test_pass
                self.test_result.request_time = http_enty.elapsed.total_seconds()
                if is_save:
                    self.test_result.save()
                return {"msg": "status_code %s /n,response body:%s，" % (http_enty.status_code, response_text), "retcode": 0}

            else:
                print("没有找到用例ITest header %s" % self.test_result.header_id)
                return {"msg": "没有找到用例ITest header %s" % self.test_result.header_id}

        else:
            print("没有找到用例ITest id %s" % self.test_result.itest_id)
            return {"msg": "没有找到用例ITest id %s" % self.test_result.itest_id}

    def init_replace_data(self, itest):
        is_data_exist = False
        repalcer = BeforTest.objects.filter(replace_name=str(itest.replace_name).strip())
        if len(repalcer) > 0:
            if repalcer[0].replace_update_time == '' or repalcer[0].replace_update_time is None:
                # 如果默认没有数据的，初始化数据一下
                phone_star = "171"
                phone_random = random.randint(10000000, 99999999)
                phone_all = phone_star + str(phone_random)
                repalcer[0].replace_data = phone_all
                self.replace_data = phone_all
                repalcer[0].replace_update_time = datetime.datetime.now()
                repalcer[0].save()

            else:
                current_time = datetime.datetime.now()
                print("当前时间 %s" % current_time)
                print("数据库字段时间 %s" % repalcer[0].replace_update_time)
                if (current_time - repalcer[0].replace_update_time).seconds > 120:
                    phone_star = "171"
                    phone_random = random.randint(10000000, 99999999)
                    phone_all = phone_star + str(phone_random)
                    self.replace_data = phone_all
                    repalcer[0].replace_data = phone_all
                    repalcer[0].replace_update_time = datetime.datetime.now()
                    repalcer[0].save()
                else:
                    # 如果小于2小时候的，直接读取替换表中数据
                    self.replace_data = repalcer[0].replace_data
        else:
            # 查询无数据时候，更新一条
            phone_star = "171"
            phone_random = random.randint(10000000, 99999999)
            phone_all = phone_star + str(phone_random)
            bt = BeforTest(replace_name="{{phone}}", replace_data=phone_all, replace_update_time=datetime.datetime.now())
            self.replace_data = phone_all
            bt.save()
