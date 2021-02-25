from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from iface.models import *
import json
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from .http_ import HttpEntiry
from .http_ import TestHttpEntiry
from .common_ import *
from .Views import TestResultView


def testview(request):

    return HttpResponse("hallo")


def root(request):
    return render(request, 'index.html')


def go_add_header(request):
    """添加头部页面"""
    return render(request, 'add_header.html')


def go_add_suit(request):
    """添加业务"""
    return render(request, 'add_suit.html')


def go_add_test(request):
    """添加测试用例"""
    return render(request, 'add_test.html')


def go_run(request):
    """选择用例，创建运行集合"""
    return render(request, 'go_run.html')


def save_header(request):
    """添加头部"""
    if request.method == 'POST':
        data = json.loads(request.body)
        header_name = data.get('header_name', None)
        header_value = data.get('header_value', None)
    else:
        return JsonResponse({"msg": "不支持非post"})

    header_all = HeaderManager.objects.filter(header_name=header_name)
    for h in header_all:
        print(h.header_name)
        print(h.value)

    if str(header_name).strip() == "" or str(header_value).strip() == "":
        return JsonResponse({"msg": "名称或值为空，不给保存"})

    if len(header_all) > 0:
        return JsonResponse({"msg": "名称重复，不给保存"})

    header = HeaderManager(header_name=header_name, value=header_value)
    try:
        header.save()
    except Exception as e:
        return JsonResponse({"msg": "异常%s" % e})

    return JsonResponse({"msg": "添加成功"})


def get_headers(request):
    """返回所有头部"""
    lst = []
    header_all = HeaderManager.objects.all()
    for h in header_all:
        temp = {}
        temp['h_name'] = h.header_name
        temp['h_v'] = h.value
        temp['h_id'] = h.id
        lst.append(temp)
    return JsonResponse({"data": lst})


def save_suit(request):
    """添加业务"""

    suit_name = None

    if request.method == 'POST':
        data = json.loads(request.body)
        suit_name = data.get('suit_name', None)
    else:
        return JsonResponse({"msg": "不支持非post"})

    lst = {}

    suit_all = TestSuit.objects.filter(suit_name=str(suit_name).strip())
    for h in suit_all:
        print(h.suit_name)

    if suit_name is None:
        return JsonResponse({"msg": "业务名称为None，添加失败"})

    if str(suit_name).strip() == "":
        return JsonResponse({"msg": "业务名称为空格，添加失败"})

    if len(suit_all) > 0:
        return JsonResponse({"msg": "名称重复，添加失败"})

    suit = TestSuit(suit_name=suit_name, is_able=True)
    try:
        suit.save()
    except Exception as e:
        return JsonResponse({"msg": "异常%s" % e})

    return JsonResponse({"msg": "添加成功"})


def get_suit(request):
    """返回所有业务名称"""
    lst = []
    s_all = TestSuit.objects.all()
    for h in s_all:
        temp_dict = {}
        temp_dict['s_name'] = h.suit_name
        temp_dict['s_id'] = h.id
        lst.append(temp_dict)

    return JsonResponse({"data": lst})


def get_test(request):
    """返回所有用例"""
    lst = []
    s_all = ITest.objects.all()
    for h in s_all:
        temp_dict = {}
        temp_dict['s_name'] = h.suit_name
        temp_dict['s_id'] = h.id
        lst.append(temp_dict)

    return JsonResponse({"data": lst})


def save_test(request):
    """添加用例"""

    if request.method == 'POST':
        data = json.loads(request.body)
        suit_id = data.get('suit_id', None)
        test_name = data.get('i_name', None)
        test_url = data.get('i_url', None)
        test_method = data.get('i_method', None)
        test_header = data.get('i_header', None)
        test_json = data.get('i_json', None)
        test_data = data.get('i_data', None)
        test_source_address = data.get('i_source_address', None)
        test_expected = data.get('i_expected', None)
        test_match_type = data.get('i_match_type', None)
        test_replace = data.get('i_replace', None)

    else:
        return JsonResponse({"msg": "不支持非post"})

    if (suit_id is not None)and (test_name is not None) and (test_url is not None) and (test_method is not None) and (test_header is not None) and (test_expected is not None) and (test_match_type is not None):
        test_all = ITest.objects.filter(case_name=str(test_name).strip())

        if len(test_all) > 0:
            return JsonResponse({"msg": "test_name 名称重复，添加失败"})

        test = ITest(case_name=test_name, case_url=test_url, case_method=test_method, case_header_id=test_header, case_json=test_json, case_data=test_data, case_expected=test_expected, source_address=test_source_address, suit_id=suit_id, is_able=True, result_match_type=test_match_type, replace_name=test_replace)
        try:
            test.save()
        except Exception as e:
            return JsonResponse({"msg": "异常%s" % e})
        return JsonResponse({"msg": "保存成功"})
    else:
        return JsonResponse({"msg": "有数据为空，请检查"})


def test_test(request):
    """检查新加的是否可用"""

    if request.method == 'POST':
        data = json.loads(request.body)
        suit_id = data.get('suit_id', None)
        test_name = data.get('i_name', None)
        test_url = data.get('i_url', None)
        test_method = data.get('i_method', None)
        test_header = data.get('i_header', None)
        test_json = data.get('i_json', None)
        test_data = data.get('i_data', None)
        test_source_address = data.get('i_source_address', None)
        test_expected = data.get('i_expected', None)
        test_match_type = data.get('i_match_type', None)
        test_replace = data.get('i_replace', None)

    else:
        return JsonResponse({"msg": "不支持非post"})

    # print("%s %s %s %s %s" % (test_url, test_method, test_header, test_expected, test_match_type))
    # print(test_url and test_method and test_header and test_expected and test_match_type)
    if (test_url is not None) and (test_method is not None) and (test_header is not None) and (test_expected is not None) and (test_match_type is not None):

        itest = ITest(case_name=test_name, case_url=test_url, case_method=test_method, case_header_id=test_header, case_json=test_json, case_data=test_data, case_expected=test_expected, source_address=test_source_address, suit_id=suit_id, is_able=True, result_match_type=test_match_type, replace_name=test_replace)
        response = TestHttpEntiry().run_test_without_save(itest)
        if response:
            return JsonResponse({"msg": "测试成功"})
        else:
            return JsonResponse({"msg": "测试失败"})
    else:
        return JsonResponse({"msg": "有数据为空，请检查 %s" % request.body})


def get_run(request):
    """通过运行集id，获取用例list"""
    run_id = None
    if request.method == 'POST':
        if not request.body:
            return JsonResponse({"msg": "没有参数"})
        data = json.loads(request.body)
        if "run_id" in data:
            run_id = data.get('run_id', None)

    lst = []
    print(run_id)
    if run_id is not None:
        test_set_all = TestResult.objects.filter(run_id=int(run_id))
        lst2 = []
        for t in test_set_all:
            i_test = ITest.objects.filter(id=t.itest_id)
            if len(i_test) > 0:
                temp_dict = {}

                temp_dict['t_id'] = i_test[0].id
                temp_dict['t_name'] = i_test[0].case_name
                temp_dict['t_url'] = i_test[0].case_url
                temp_dict['t_method'] = "GET" if i_test[0].case_method == HttpMethod.GET.value else "POST"

                t_h = HeaderManager.objects.filter(id=i_test[0].case_header_id)

                temp_dict['t_header_name'] = t_h[0].header_name
                temp_dict['t_json'] = i_test[0].case_json
                temp_dict['t_data'] = i_test[0].case_data
                temp_dict['t_expected'] = i_test[0].case_expected
                temp_dict['t_source_address'] = i_test[0].source_address
                temp_dict['t_able'] = i_test[0].is_able

                suit_all = TestSuit.objects.filter(id=i_test[0].suit_id)
                temp_dict['t_suit_name'] = suit_all[0].suit_name

                temp_dict['t_match_type'] = "相等" if i_test[0].result_match_type == MatchMethod.EQAUL.value else "包含"
                temp_dict['t_replace_name'] = i_test[0].replace_name
                lst2.append(temp_dict)
        return JsonResponse({"data": lst2})

    s_all = TestRun.objects.all()
    for h in s_all:
        temp_dict = {}
        temp_dict['r_id'] = h.id
        temp_dict['r_name'] = h.run_name
        lst.append(temp_dict)

    return JsonResponse({"data": lst})


def add_run(request):
    """添加运行集合，一个运行集合是一次勾选可用用例，一起跑"""
    if request.method == 'POST':
        if not request.body:
            return JsonResponse({"msg": "请勾选用例"})
        data = json.loads(request.body)
        if "test_ids" in data:
            test_lst = data.get('test_ids', None)
        else:
            return JsonResponse({"msg": "勾选的用例为空，添加失败"})
        if "run_name" in data:
            run_name = data.get('run_name', None)
        else:
            return JsonResponse({"msg": "运行集名称为空，添加失败"})
    else:
        return JsonResponse({"msg": "不支持非post"})

    if len(test_lst) == 0:
        return JsonResponse({"msg": "勾选的用例=0，添加失败"})

    run_ids = ""
    for test_id in test_lst:
        run_ids += str(test_id) + "#"

    try:
        # 运行集合，自增1就好
        t_run = TestRun(run_name=run_name, run_ids=run_ids)
        t_run.save()
    except Exception as e:
        return JsonResponse({"msg": "异常%s" % e})

    return JsonResponse({"msg": "添加运行集成功"})


@require_POST
def run_result(request):
    """通过运行id，执行结果集"""
    if not request.body:
        return JsonResponse({"msg": "请勾选用例"})
    data = json.loads(request.body)
    if "run_id" in data:
        run_id = data.get('run_id', None)
    else:
        return JsonResponse({"msg": "运行集，选择为空，执行结果失败"})

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
        # 逆序，去第一个作为历史counter，新的counter + 1
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
        return JsonResponse({"msg": "执行完毕"})
    else:
        return JsonResponse({"msg": "没有找到运行集，执行结果失败"})


@require_POST
def get_test_result(request):
    return TestResultView.TestTesultView().get_test_result(request)


def get_test(request):
    """查询用例"""

    lst = []
    test_all = ITest.objects.all()
    for t in test_all:
        temp_dict = {}

        temp_dict['t_id'] = t.id
        temp_dict['t_name'] = t.case_name
        temp_dict['t_url'] = t.case_url
        temp_dict['t_method'] = "GET" if t.case_method == HttpMethod.GET.value else "POST"

        t_h = HeaderManager.objects.filter(id=t.case_header_id)

        temp_dict['t_header_name'] = t_h[0].header_name
        temp_dict['t_json'] = t.case_json
        temp_dict['t_data'] = t.case_data
        temp_dict['t_expected'] = t.case_expected
        temp_dict['t_source_address'] = t.source_address
        temp_dict['t_able'] = t.is_able

        suit_all = TestSuit.objects.filter(id=t.suit_id)
        temp_dict['t_suit_name'] = suit_all[0].suit_name

        temp_dict['t_match_type'] = "相等" if t.result_match_type == MatchMethod.EQAUL.value else "包含"
        temp_dict['t_replace_name'] = t.replace_name

        lst.append(temp_dict)

    return JsonResponse({"data": lst})


