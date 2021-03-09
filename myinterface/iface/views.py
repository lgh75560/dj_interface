from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from iface.models import *
import json
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from .http_ import HttpEntiry
from .common_ import *
from .Views import ViewTest
from .Views import ViewTestResult
from django.core.paginator import Paginator
from .Views import ViewRunResult
from .Views import ViewTimer


server_host = ""


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

    real_header = header_value
    if not str(header_value).startswith("{"):
        real_header = "{" + header_value
    if not str(header_value).endswith("}"):
        real_header = real_header + "}"
    try:
        dict_header = eval(real_header)
    except Exception as ee:
        return JsonResponse({"msg": "转化dict字典报错，无法存储成功，请重新检查在线json %s" % ee, 'retcode': -1})

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
    data = json.loads(request.body)
    server_host = request.META['REMOTE_HOST']
    print(server_host)
    current_page = data.get('currentPage', None)
    page_size = data.get('PageSize', None)
    print(current_page)
    print(page_size)
    if current_page is None or page_size is None:
        return JsonResponse({"msg": "current_page or page_size 为空", "retcode": -1})

    lst = []

    s_all = ITest.objects.all()

    # #设置每一页显示几条  创建一个panginator对象
    ptr = Paginator(s_all, page_size)

    s_all = ptr.page(current_page)

    for h in s_all:
        temp_dict = {}
        temp_dict['s_name'] = h.suit_name
        temp_dict['s_id'] = h.id
        lst.append(temp_dict)

    return JsonResponse({"data": lst})


def update_test(request):
    return ViewTest.TestManager().update_test(request)


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
        itest_result = TestResult()
        return JsonResponse((HttpEntiry(itest_result).run_test(is_save=False, itest=itest)))
    else:
        return JsonResponse({"msg": "有数据为空，请检查 %s" % request.body})


def get_run_select(request):
    """运行集合，按run id生成的多个结果"""
    return ViewRunResult.RunResult().get_run_select(request)


def get_run_report(request):
    """运行集合，按run id + counter 获取报告"""
    return ViewRunResult.RunResult().get_report(request)


def get_run(request):
    """通过运行集id，获取用例list"""
    run_id = None
    if request.method == 'POST':
        if not request.body:
            return JsonResponse({"msg": "没有参数"})
        data = json.loads(request.body)
        if "run_id" in data:
            run_id = data.get('run_id', None)
            run_counter = data.get('run_counter', None)

    lst = []
    print(run_id)
    # 适配有run id的情况，不要配置else
    if run_id is not None and str(run_id).strip() != "":
        test_set_all = TestResult.objects.filter(run_id=int(run_id), run_counter=run_counter)
        lst2 = []
        for t in test_set_all:
            try:
                i_test = ITest.objects.get(id=t.itest_id)
                dict_result = i_test.to_dict()

                result_match_type = dict_result["result_match_type"]
                dict_result["result_match_type"] = "相等" if result_match_type == MatchMethod.EQAUL.value else "包含"

                test_method = dict_result['case_method']
                dict_result['case_method'] = "GET" if test_method == HttpMethod.GET.value else "POST"

                t_h = HeaderManager.objects.filter(id=i_test.case_header_id)

                dict_result['case_header_name'] = t_h[0].header_name

                suit_all = TestSuit.objects.filter(id=i_test.suit_id)

                dict_result['case_suit_name'] = suit_all[0].suit_name

                lst2.append(dict_result)
            except Exception as e1:
                pass
        return JsonResponse({"data": lst2})

    # 还有一个全部查询返回结果的
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
    return ViewRunResult.RunResult().run_run(request)


@require_POST
def get_test_result(request):
    return ViewTestResult.TestTesultView().get_test_result(request)


def get_test_from_info(request):
    return ViewTest.TestManager().get_test_from_info(request)


def get_test_list(request):
    """查询用例"""
    if request:

        current_page = request.GET.get('currentPage', None)
        page_size = request.GET.get('PageSize', None)
        suit = request.GET.get('suit', None)
        # print("current_page" + current_page)
        # print("page_size" + page_size)
        # print("suit %s" % suit)
    else:
        return JsonResponse({"msg": "current_page or page_size 为空", "retcode": -1})
    if current_page is None or page_size is None:
        return JsonResponse({"msg": "current_page or page_size 为空", "retcode": -1})

    lst = []
    if suit is not None:

        s_all = ITest.objects.filter(suit_id=suit)
    else:
        s_all = ITest.objects.all()

    # #设置每一页显示几条  创建一个panginator对象
    ptr = Paginator(s_all, page_size)

    s_all = ptr.page(current_page)
    print("总数 %s" % ptr.count)
    print("page_range %s" % ptr.page_range)
    print("num_pages %s" % ptr.num_pages)
    for t in s_all:
        dict_result = t.to_dict()

        result_match_type = dict_result["result_match_type"]
        dict_result["result_match_type"] = "相等" if result_match_type == MatchMethod.EQAUL.value else "包含"

        test_method = dict_result['case_method']
        dict_result['case_method'] = "GET" if test_method == HttpMethod.GET.value else "POST"

        t_h = HeaderManager.objects.filter(id=t.case_header_id)

        dict_result['case_header_name'] = t_h[0].header_name

        suit_all = TestSuit.objects.filter(id=t.suit_id)

        dict_result['case_suit_name'] = suit_all[0].suit_name

        lst.append(dict_result)

    return JsonResponse({"data": lst, "retcode": 0, "max_page_num": ptr.num_pages, "total": ptr.count})


def add_timer_job(request):
    """添加job"""
    return ViewTimer.TimerView().add_timer_job(request)


def get_timer_jobs(request):
    """查询job"""
    return ViewTimer.TimerView().get_all_job()


def del_timer_jobs(request):
    """删除job"""
    return ViewTimer.TimerView().remove_job(request)