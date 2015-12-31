#Borrow Books

# -*- coding: utf-8 -*-
__author__="pengzhen3"

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import configparser

config=configparser.ConfigParser()
#IpConfig.ini可以是一个不存在的文件，意味着准备新建配置文件。
config.read("BookConfig.ini")


mail_to = config.get("EmailConfig","mail_to")
mail_host = "smtp.hikvision.com.cn"
mail_user = config.get("EmailConfig","mail_user")
mail_pass = config.get("EmailConfig","mail_pass")
mail_postfix="hikvision.com.cn"  #发件箱的后缀
mailto_list=[mail_to]
  
def send_mail(to_list,sub,content):
    me ="hello"+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.quit()  
        return True  
    except Exception as e:  
        print("Exception:",e)  
        return False 

if __name__ == '__main__':  
    if send_mail(mailto_list,"【图书管理】","【该还书了！】"):  
        print("发送成功")  
    else:  
        print("发送失败")
