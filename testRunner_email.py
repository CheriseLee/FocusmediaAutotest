# -*- coding:utf-8 -*-
# author by lihuanhuan

'''组织测试用例,运行测试程序'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from BSTestRunner import *
import unittest
import pytest


def send_mail(latest_report):
    # 获取最新报告，以二进制方式打开测试报告
    f = open(latest_report, 'rb')
    send_file = f.read()
    f.close()
    # 发送邮箱服务器
    smtpserver = 'smtp.163.com'

    # 发送邮箱及授权密码
    user = 'lihh0727@163.com'
    password = 'lihh0727'

    # 发送邮箱和接收邮箱
    sender = 'lihh0727@163.com'
    receives = ['463836190@qq.com', 'lihuanhuan@focusmedia.cn']

    # 邮件主题和内容
    subject = 'KUMA计划单元接口自动化测试报告'
    content = '<html><h1 style="color:res">请查看附件</h1></html>'
    # 邮件正文,定义附件
    att = MIMEText(send_file, 'base64', 'utf-8')
    att['Content-Type'] = 'application/octet-stream'
    # 附件命名,获取当前时间
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    att['Content-Disposition'] = ("attachment;filename=ad_Group_TestReport_%s.html")%now

    msgRoot = MIMEMultipart()
    msgRoot.attach(MIMEText(content, 'html', 'utf-8'))
    msgRoot['Subject'] = subject
    msgRoot['From'] = sender
    msgRoot['To'] = ','.join(receives)
    msgRoot.attach(att)

    # SSL协议端口号,不同邮箱端口不同
    smtp = smtplib.SMTP_SSL(smtpserver, 465)
    # 向服务器标识用户身份
    smtp.helo(smtpserver)
    # 服务器返回结果确认
    smtp.ehlo(smtpserver)
    # 登录邮箱服务器用户名密码
    smtp.login(user, password)

    print("Start send Email...")
    smtp.sendmail(sender, receives, msgRoot.as_string())
    smtp.quit()
    print("Send success")


def latest_report(report_dir):
    lists = os.listdir(report_dir)
    # 按时间顺序对文件排序
    lists.sort(key=lambda fn: os.path.getatime(report_dir + '\\'))
    # print(lists)
    # print("latest report is:" + lists[-3])
    # 输出最新报告路径
    file = os.path.join(report_dir, lists[-3])
    # print(file)
    return file


def test_suite():
    # 定义测试用例集

    dir_path = os.path.abspath('.')
    test_dir = dir_path + '\\testCase\\campaign\\'
    discover = unittest.defaultTestLoader.discover(test_dir, pattern="test*.py")

    # 存放报告的文件夹
    report_dir = dir_path + '\\testReport\\'
    # 报告命名时间格式化
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    # 报告文件完整路径
    report_name = report_dir + '/' + now + 'result.html'

    # 打开文件在报告文件写入测试结果
    with open(report_name, 'wb') as f:
        runner = BSTestRunner(stream=f, title="Test Report", description="test case result")
        runner.run(discover)
    f.close()

    latestReport = latest_report(report_dir)
    send_mail(latestReport)


if __name__ == '__main__':
    # test_suite()
    pytest.main(['testCase/campaign/test_campaign_list.py','--alluredir','testReport/reportallure/'])
