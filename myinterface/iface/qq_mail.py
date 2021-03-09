import smtplib
import time
from email.mime.text import MIMEText
import platform
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import xlrd


class SendMail:

    def send_report_with_dict(self, title, case_list, to_mail, total, pass_count, fail_count, attach_url):
        msg_from = '3012328624@qq.com'  # 发送方邮箱
        passwd = 'hewpangxataidfdj'  # 填入发送方邮箱的授权码
        msg_to = to_mail

        subject = title + str(time.strftime('%Y-%m-%d', time.localtime(time.time())))  # 主题

        html = ""
        add_str = ""
        row_list = []
        need_header = ["request_data", "result_pass", "case_expected", "case_name", "case_url", 'result_match_type', "suit_name"]
        true_header = []
        is_init = False
        # 获取 用例list
        for case in case_list:
            current_case_lst = []
            for k, v in case.items():
                if str(k) in need_header:
                    if k not in true_header:
                        true_header.append(k)

                    current_case_lst.append(v)
                is_init = True

            row_list.append(current_case_lst)
        print(true_header)
        _tr = self.generate_tr(row_list, true_header)

        html = """
                    <html>
                        <style>
                            body{ font-family: verdana, arial, helvetica, sans-serif; font-size: 80%%; }
                            td{max-width: 200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;margin-left: 2em;}
                            .tr2{background-color: #c60;}
                            table{font-size:100%%;}
                            .red{max-width: 100px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;background:red;}
                            .green{max-width: 100px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;background:green;}
                        </style>
                        <div> 
                            <h2>用例总数：%(total)s，通过数量：%(pass_count)s，失败数量：%(fail_count)s</h2>
                            <a href='%(url)s'>报告地址 %(url)s</a>
                        </div>
                        <table >
                            %(tr)s
                        </table>
                    </html>
                    """

        html = html % dict(tr=_tr, total=total, pass_count=pass_count, fail_count=fail_count, url=attach_url)
        add_str += html
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = msg_from
        msg['To'] = msg_to

        # 支持附件的方法
        message = MIMEMultipart(
            "alternative", None, [MIMEText(add_str, 'html')])

        # 添加附件
        msg.attach(message)

        try:
            s = smtplib.SMTP("smtp.qq.com", 25)
            s.login(msg_from, passwd)
            s.sendmail(msg_from, msg_to.split(","), msg.as_string())
            print("发送成功")

        except Exception as rtrt:
            print("发送失败")

    def generate_tr(self, _list, _header_lst):
        out_str = "<tr class='tr2'>"
        for yy in _header_lst:
            out_str += "<td>" + str(yy) + "</td>"
        out_str += "</tr>"

        for kk in range(0, len(_list)):
            out_str += "<tr>"
            for yy in range(0, len(_list[kk])):
                if (_list[kk][yy]) is True:
                    out_str += "<td class='green'>" + str(_list[kk][yy]) + "</td>"
                    continue
                if (_list[kk][yy]) is False:
                    out_str += "<td class='red'>" + str(_list[kk][yy]) + "</td>"
                    continue
                out_str += "<td>" + str(_list[kk][yy]) + "</td>"
            out_str += "</tr>"
        return out_str
