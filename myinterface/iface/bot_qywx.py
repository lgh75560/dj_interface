# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 14:30
# @Author  : gh
# @Software: PyCharm

import requests
import json


class QywxBot:
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=fe746757-914b-4b24-86b6-106f9c5b5c0a"

    url_test_group_use = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=36b4e581-3068-4280-8caf-7cf69612457d"

    headers = {
        "Content-Type": "application/json;charset=utf-8"
    }

    def send_text(self, type_text, pass_count, fail_count, fail_list):

        fail_str = ""
        count = 0
        for fail_name in fail_list:
            fail_str += "<font color=\"comment\">%s：%s</font> \n" % (count, fail_name)
            count += 1

        out_str = "出错类型：%s。用例通过数%s；用例失败数<font color=\"warning\">%s</font>。失败用例列表：\n" % (type_text, pass_count, fail_count)
        out_str += fail_str

        post_data = {
            "msgtype": "markdown",
            "markdown": {
                "content": out_str,
                "mentioned_list": ["@all"],
                "mentioned_mobile_list": ["@all"]
            }
        }

        r = requests.post(url=self.url, headers=self.headers, data=json.dumps(post_data))
        print(r.text)

    def send_text_use_test_group(self, type_text, pass_count, fail_count, fail_list, url):
        """测试组机器人用的"""
        fail_str = ""
        count = 0
        for fail_name in fail_list:
            fail_str += "<font color=\"comment\">%s：%s</font> \n" % (count, fail_name)
            count += 1

        out_str = "出错类型：%s。用例通过数%s；用例失败数<font color=\"warning\">%s</font>。失败用例列表：\n >>[点击查看报告链接](%s)\n" % (type_text, pass_count, fail_count, url)
        out_str += fail_str

        post_data = {
            "msgtype": "markdown",
            "markdown": {
                "content": out_str,
                "mentioned_list": ["@all"],
                "mentioned_mobile_list": ["@all"]
            }
        }

        r = requests.post(url=self.url_test_group_use, headers=self.headers, data=json.dumps(post_data))
        print(r.text)


if __name__ == "__main__":
    q = QywxBot()
    li = ["侧撒归属感", "噶问过"]
    q.send_text_use_test_group(type_text="是测试", pass_count=10, fail_count=6, fail_list=li, url="www.baidu.com")
