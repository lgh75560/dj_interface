from django.db import models

# Create your models here.


class ITest(models.Model):
    id = models.AutoField(primary_key=True)
    case_name = models.CharField(max_length=200)
    case_url = models.CharField(max_length=200)
    case_method = models.CharField(max_length=10)
    case_header_id = models.IntegerField()
    case_json = models.CharField(max_length=200)
    case_data = models.CharField(max_length=200)
    case_expected = models.CharField(max_length=200)
    source_address = models.CharField(max_length=50)
    # 是否可用
    is_able = models.BooleanField(null=True)
    # 单测试，靠背在测试集中
    suit_id = models.IntegerField()
    # 结果匹配，包含匹配、完全匹配
    result_match_type = models.IntegerField(null=True)
    # 被替换的变量
    replace_name = models.CharField(max_length=50)
    # 添加一个，测试类型，就是测试是否可用的时候用的，为0
    case_type = models.IntegerField(null=True)

    def to_dict(self):
        """自动转化成字典，66的"""
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class BeforTest(models.Model):
    id = models.AutoField(primary_key=True)
    # 被替换字符串  如  {{phone}}
    replace_name = models.CharField(max_length=50)
    # 替换的数据
    replace_data = models.CharField(max_length=20)
    # 更新时间，多少小时，更新一次里面的replace_data
    replace_update_time = models.DateTimeField(null=True, default=None)

    def to_dict(self):
        """自动转化成字典，66的"""
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class TestSuit(models.Model):
    id = models.AutoField(primary_key=True)
    suit_name = models.CharField(max_length=50)
    # 是否可用
    is_able = models.BooleanField(null=True)

    def to_dict(self):
        """自动转化成字典，66的"""
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class HeaderManager(models.Model):
    """头部headers管理"""
    id = models.AutoField(primary_key=True)
    header_name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    def to_dict(self):
        """自动转化成字典，66的"""
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class TestRun(models.Model):
    """
     suit < case
     testrun < testsult
    """
    # 运行id
    id = models.AutoField(primary_key=True)
    # 运行名称
    run_name = models.CharField(max_length=200)
    # 只有开始时间
    start_time = models.DateTimeField(null=True, default=None)
    end_time = models.DateTimeField(null=True, default=None)

    # 用例集合用逗号分隔
    run_ids = models.CharField(max_length=200)

    def to_dict(self):
        """自动转化成字典，66的"""
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class TestResult(models.Model):
    """
    测试结果保存
    """
    id = models.AutoField(primary_key=True)
    run_id = models.IntegerField(null=True,)
    # 同一个runid运行，不同次数，counter递增
    run_counter = models.IntegerField()
    # 关联的用例id
    itest_id = models.IntegerField()

    start_time = models.DateTimeField(null=True, default=None)
    # 结束时间
    end_time = models.DateTimeField(null=True, default=None)

    # 存储结果
    result_response = models.CharField(max_length=200)
    header_id = models.IntegerField(null=True)
    request_url = models.CharField(max_length=200)
    request_json = models.CharField(max_length=100)
    request_data = models.CharField(max_length=100)
    # 响应状态码
    response_status = models.IntegerField(null=True)
    result_pass = models.BooleanField(null=True)
    request_time = models.FloatField(null=True)
    # 可能什么都没有，这里出错误提示
    result_des = models.CharField(max_length=100)

    def to_dict(self):
        """自动转化成字典，66的"""
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])