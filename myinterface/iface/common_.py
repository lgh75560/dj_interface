# -*- coding: utf-8 -*-
# @Time    : 2021/2/8 11:26
# @Author  : gh
# @Software: PyCharm

from enum import Enum
from django import forms


class HttpMethod(Enum):
    """http类型"""
    GET = 0
    POST = 1


class MatchMethod(Enum):
    """结果匹配"""
    CONTAIN = 0
    EQAUL = 1


def check_not_none(value):
    """判断不为空，为空就是False"""
    if value in None:
        return False
    else:
        return True


class TestCaseFrom(forms.Form):
    """前端提交的表单，转化为对象"""
    """没用，这个一一对应的，改数据就麻烦"""

    suit_id = forms.IntegerField(required=True, error_messages={'required': '业务不能为空'})
    i_name = forms.CharField(required=True, error_messages={'required': '用例名称不能为空'})
    i_url = forms.CharField(required=True, error_messages={'required': 'URL不能为空'})
    i_method = forms.CharField(required=True, error_messages={'required': '请求方式不能为空'})
    i_header = forms.IntegerField(required=True, error_messages={'required': 'header不能为空'})
    i_json = forms.CharField(required=False)
    i_data = forms.CharField(required=False)
    i_expected = forms.CharField(required=True, error_messages={'required': '预期结果不能为空'})

    i_source_address = forms.CharField(required=False)

    # 结果匹配，包含匹配、完全匹配
    i_match_type = forms.IntegerField(required=True, error_messages={'required': '结果匹配方式不能为空'})
    # 被替换的变量
    i_replace = forms.CharField(required=False)

