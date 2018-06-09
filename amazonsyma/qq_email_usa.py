#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

my_sender = '820370953@qq.com'  # 发件人邮箱账号
my_pass = 'bihhclfyyqcrbeab'  # 发件人邮箱密码(当时申请smtp给的口令)


def read_content(email):
    with open('20180609_usa.txt','r',encoding='utf-8') as f:
    # with open('b.txt','r',encoding='utf-8') as f:
        content = f.read()
        ret = mail(content,email)
    return ret


def mail(content,user_email):
    ret = True
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['From'] = formataddr(["游平平", my_sender])
        # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['To'] = formataddr(["收件人昵称", user_email])
        # 邮件的主题，也可以说是标题
        msg['Subject'] = "syma产品在亚马逊美国站点的排名 --0609"
        # msg['Subject'] = "20180409Amazon单个商品追踪情况"
        # 发件人邮箱中的SMTP服务器，端口是465
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 括号中对应的是发件人邮箱账号、邮箱密码
        server.login(my_sender, my_pass)
        # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.sendmail(my_sender, [user_email, ], msg.as_string())
        # 关闭连接
        server.quit()
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret


def main():
    # 收件人邮箱列表
    # email_list = ['msqming@163.com', '2627001019@qq.com']
    # email_list = ['45751351@qq.com','783248539@qq.com',
    #               '2627001019@qq.com','249935966@qq.com',
    #               '799232857@qq.com']
    # email_list = ['msqming@163.com']
    email_list = ['songmengyue0918@dingtalk.com','xiafan2012@126.com','chengzhiwei0679@dingtalk.com'] # 吴雯霞，宋梦岳
    for email in email_list:
        ret = read_content(email)

        if ret:
            print("邮件发送成功")
        else:
            print("邮件发送失败")


if __name__ == '__main__':
    main()
